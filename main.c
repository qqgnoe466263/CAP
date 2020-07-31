#include <stdio.h>

#include "./http_server.h"
#define PORT 8000
#define IP "127.0.0.1"
int main(void)
{
    printf("Listening  on %s:%d......\n", IP, PORT);
    httpd_start(IP, PORT);
}
