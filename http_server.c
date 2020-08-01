#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <string.h>
#include <sys/stat.h>

#include "http_server.h"
#include "http_parser.h"
#define BUFSIZE 512
#define NOTFOUND "HTTP/1.1 404 Not Found\r\nServer: xiaobye-server\r\nConnection: close\r\nContent-Type: text/html; charset=iso-8859-1\r\nContent-Length: 9\r\n\r\nNot Found"
#define OK "HTTP/1.1 200 OK\r\nServer: xiaobye-server\r\nContent-Type: text/html; charset=UTF-8\r\nConnection: close\r\n"
#define CONTENTLENGTH "Content-Length: %ld\r\n"
char filename[BUFSIZE];
int on_message_begin(http_parser* _) {
  (void)_;
  printf("\n***MESSAGE BEGIN***\n\n");
  return 0;
}

int on_headers_complete(http_parser* _) {
  (void)_;
  printf("\n***HEADERS COMPLETE***\n\n");
  return 0;
}

int on_message_complete(http_parser* _) {
  (void)_;
  printf("\n***MESSAGE COMPLETE***\n\n");
  return 0;
}


int on_url(http_parser* _, const char* at, size_t length) {
  (void)_;
  int i;
  int found=0;
  printf("Url: %.*s\n", (int)length, at);
  for(i=0;i<length;i++){
	if(at[i]=='?'){
		i++;
		found = 1;
		break;
	}
  }
  if(found){
	strncpy(filename,&at[i],length-i);
	filename[length-i]='\0';
	printf("filename: %s\n",filename);
  }else{
	filename[0]='\0';
  }
  return 0;
}

int on_header_field(http_parser* _, const char* at, size_t length) {
  (void)_;
  printf("Header field: %.*s\n", (int)length, at);
  return 0;
}

int on_header_value(http_parser* _, const char* at, size_t length) {
  (void)_;
  printf("Header value: %.*s\n", (int)length, at);
  return 0;
}

int on_body(http_parser* _, const char* at, size_t length) {
  (void)_;
  printf("Body: %.*s\n", (int)length, at);
  return 0;
}
void process_request(int clifd){
	ssize_t n;
	char buf[BUFSIZE];
	char *filebuf;
	static http_parser *parser;
	char *respbuf;
	long fsize;
	FILE * f;
	struct stat path_stat;
    http_parser_settings parser_set;	
    parser_set.on_message_begin = on_message_begin;
    parser_set.on_header_field = on_header_field;
    parser_set.on_header_value = on_header_value;
    parser_set.on_url = on_url;
    parser_set.on_body = on_body;
    parser_set.on_headers_complete = on_headers_complete;
    parser_set.on_message_complete = on_message_complete;

	n = recv(clifd,buf,10240,0);
/*	printf("%d\n",n);
	buf[n]='\0';
	printf("%s\n",buf);
	printf("%d\n",strlen(buf));
*/	
	//parse http request

	parser = (http_parser*)malloc(sizeof(http_parser)); 
			 
	http_parser_init(parser, HTTP_REQUEST); 
	http_parser_execute(parser, &parser_set, buf, strlen(buf));

	//http response
	stat(filename, &path_stat);
	if(!S_ISREG(path_stat.st_mode)|((f = fopen(filename, "rb"))==NULL)){
		send(clifd,NOTFOUND,sizeof(NOTFOUND),0);
		free(parser);
		parser=NULL;
		shutdown(clifd,SHUT_RDWR);
		close(clifd);
		return;
	}
	fseek(f, 0, SEEK_END);
	fsize = ftell(f);
	fseek(f, 0, SEEK_SET);  /* same as rewind(f); */

	filebuf = malloc(fsize + 1);
	fread(filebuf, 1, fsize, f);
	filebuf[fsize]='\0';
	fclose(f);

	
	char content_len[BUFSIZE];

	n = snprintf(content_len,BUFSIZE,CONTENTLENGTH,fsize);
	printf("%s\n",content_len);
	int resp_n = n+fsize+2+sizeof(OK);
	respbuf = malloc(resp_n+1);
	snprintf(respbuf,resp_n,"%s%s%s%s",OK,content_len,"\r\n",filebuf);
	printf("%s",respbuf);
	send(clifd,respbuf,resp_n,0);
 
	free(respbuf);
	free(filebuf);	
	free(parser);
	parser = NULL;

	close(clifd);
}
void httpd_start(const char* ip,unsigned short port){
	struct sockaddr_in addr;
	int clientfd,optval;
	int addrlen = sizeof(addr); 
	int serverfd;

	//create socket 
	if((serverfd = socket(AF_INET,SOCK_STREAM,0))==0){
		perror("socket(): ");
		exit(1);
	}
	//set socket 
	optval=1;
	setsockopt(serverfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
	setsockopt(serverfd, SOL_TCP,TCP_NODELAY,&optval, sizeof(optval));
	//init address
	addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(ip);
    addr.sin_port = htons(port);
	//bind socket
	if(bind(serverfd,(struct sockaddr*)&addr,sizeof(addr))<0){
		perror("bind(): ");
		exit(1);
	}
	//listen on socket
	if(listen(serverfd,5)<0){
		perror("bind(): ");
		exit(1);
	}

	while(1){
		if ((clientfd = accept(serverfd, (struct sockaddr *)&addr,(socklen_t*)&addrlen))<0) {
			perror("accept():");
			exit(1);
		}
		printf("Connetion in.\n");
		process_request(clientfd);

	}
}


