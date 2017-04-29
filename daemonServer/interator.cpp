#include <iostream>
#include <netinet/in.h>
#include <netdb.h>
#include <string>
#include <iostream>
#include <cstdlib>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <unistd.h>
#include "ups.pb.h"
#include "auxiliary.h"
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/text_format.h>

#define SERVERPORT 12345
#define BUFSIZE 1024

int SERVER_SOCK;

using namespace std;
using namespace gpb_ups;
using namespace google::protobuf::io;

google::protobuf::uint32 readHdr(char *buf){
  google::protobuf::uint32 size;
  google::protobuf::io::ArrayInputStream ais(buf,10);
  CodedInputStream coded_input(&ais);
  coded_input.ReadVarint32(&size);

  return size;
}


template<typename T> void readMesg(int server_sock, google::protobuf::uint32 size, T &response){
  char recv_buf[size+4];
  int byteread = 0;
  
  if((byteread = recv(server_sock, recv_buf, size+4, 0)) < 0){
    perror("read failed");
    exit(EXIT_FAILURE);
  }
  ArrayInputStream *aos1 = new ArrayInputStream(recv_buf, size+4);
  recvMesgFrom<T> (response, aos1);

  return;
}

void socketInit(){
  struct sockaddr_in server;
  struct hostent *hp;
  int server_sock;
  string message;

  server.sin_family = AF_INET;
  hp = gethostbyname("localhost");
  if(hp == 0){
    perror("gethostbyname failed");
    exit(EXIT_FAILURE);
  }
  memcpy(&server.sin_addr, hp->h_addr, hp->h_length);
  server.sin_port = htons(SERVERPORT);

  /* create server_sock for connecting to server */
  server_sock = socket(AF_INET, SOCK_STREAM, 0);
  if(server_sock < 0){
    perror("create socket failed");
    exit(EXIT_FAILURE);
  }

  /* call connect */
  if(connect(server_sock, (struct sockaddr*)&server, sizeof(server)) != 0){
    perror("connect failed");
    exit(EXIT_FAILURE);
  }

  /* construct message */
  UConnect command;
  command.set_reconnectid(1001);

  /* serialize and encode */
  int msg_size = command.ByteSize();
  msg_size += CodedOutputStream::VarintSize32(msg_size);
  char *buffer = new char[msg_size];
  ArrayOutputStream *aos = new ArrayOutputStream(buffer, msg_size);
  sendMesgTo<UConnect> (command, aos);
   
  /* send command */
  if(send(server_sock, buffer, msg_size, 0) < 0){
    perror("send failed");
    exit(EXIT_FAILURE);
  }
  //DEBUG
  cout << "Send message: " << command << endl;

  /* read response */  
  char bufferHdr[4];
  int byteread = 0;
  UConnected response;
  //Need revise, assume the encoding take 4 bytes
  if((byteread = recv(server_sock, bufferHdr, 4, MSG_PEEK)) < 0){
    perror("read failed");
    exit(EXIT_FAILURE);
  }
  int resp_size = readHdr(bufferHdr);
  readMesg<UConnected> (server_sock, resp_size, response);
  //DEBUG
  cout << "Read message: " << response << endl;
  delete []buffer;
  
  /*******************************************************/
  /* receive request from Amazon, spawn a new thread to deal with it */

  /* If the response is a pickup request, send the truck */
  UGoPickup *pickup;
  UCommands commands;
  commands.set_simspeed(5000);
  pickup = commands.add_pickups();
  pickup->set_truckid(0);
  pickup->set_whid(0);
  msg_size = commands.ByteSize();
  msg_size += CodedOutputStream::VarintSize32(msg_size);
  buffer = new char[msg_size];
  ArrayOutputStream *aos2 = new ArrayOutputStream(buffer, msg_size);
  sendMesgTo<UCommands> (commands, aos2);
  
  /* send command */
  if(send(server_sock, buffer, msg_size, 0) < 0){
    perror("send failed");
    exit(EXIT_FAILURE);
  }
  //DEBUG
  cout << "Send message: " << commands << endl;
  
  /* read response */
  UResponses responses;
  //Need revise, assume the encoding take 4 bytes
  if((byteread = recv(server_sock, bufferHdr, 4, MSG_PEEK)) < 0){
    perror("read failed");
    exit(EXIT_FAILURE);
  }
  resp_size = readHdr(bufferHdr);
  readMesg<UResponses> (server_sock, resp_size, responses);
  //DEBUG
  cout << "Read message: " << responses << endl;
  delete []buffer;
    
  close(server_sock);
  
  return;
}

int main(int argc, char **argv) {
  socketInit();
  
  return 0;
}
