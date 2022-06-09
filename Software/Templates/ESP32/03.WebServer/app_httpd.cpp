#include "esp_http_server.h"
#include <Arduino.h>
#include <ArduinoJson.h>

/*
 *  GET /isAlive
 */
esp_err_t handler_is_alive(httpd_req_t *req){
  const char resp[] = "{'status': 'OK'}";
  esp_err_t res = httpd_resp_send(req, resp, strlen(resp));
  
  printf("\n   Request \"GET /isAlive\" was served\n\n", "");    
  
  return res;
}

/*
 * POST /echoBack
 */
esp_err_t handler_echo_back(httpd_req_t *req){
    char content[100];

    /* Truncate if content length larger than the buffer */
    size_t recv_size = min(req->content_len, sizeof(content));
    
    int ret = httpd_req_recv(req, content, recv_size);

    // if the "data" attribute in the payload is not String, like "5" then
    // Guru Meditation Error: Core  1 panic'ed (LoadProhibited). Exception was unhandled. happens
    // I can not handle it
    
    const char* retData;
    if(ret > 0){
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, content);
      if (error) {
        retData = "n/a";
      } else {
          retData = doc["data"];
          retData = retData == NULL ? "wd": retData;
      }  
        
    }else{   //if (ret <= 0) {  /* 0 return value indicates connection closed */
        
        /* Check if timeout occurred */
        if (ret == HTTPD_SOCK_ERR_TIMEOUT) {
            /* In case of timeout one can choose to retry calling
             * httpd_req_recv(), but to keep it simple, here we
             * respond with an HTTP 408 (Request Timeout) error */
            httpd_resp_send_408(req);
        }
        
        /* In case of error, returning ESP_FAIL will
         * ensure that the underlying socket is closed */
        return ESP_FAIL;
    }

    String respBody;
    StaticJsonDocument<1024> ans;
    ans["data"] = retData;
    serializeJson(ans, respBody);

    const char* resp = respBody.c_str();
    esp_err_t res = httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
  
    printf("\n   Request \"POST /echoBack\" was served\n\n", "");    
  
  return res;
}

httpd_handle_t startWebServer(){
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();

    httpd_handle_t server = NULL;
    
    httpd_uri_t uri_get_is_alive = {
        .uri       = "/isAlive",
        .method    = HTTP_GET,
        .handler   = handler_is_alive,
        .user_ctx  = NULL
    };

    httpd_uri_t uri_post_echo_back = {
        .uri       = "/echoBack",
        .method    = HTTP_POST,
        .handler   = handler_echo_back,
        .user_ctx  = NULL
    };
    
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_register_uri_handler(server, &uri_get_is_alive);
        httpd_register_uri_handler(server, &uri_post_echo_back);
    }

    printf("==================================================\n");
    printf("Starting web server on port: '%d'\n", config.server_port);
    printf("         %s", "GET /isAlive\n");
    printf("         %s", "POST --data {\"data:\" \"5\"} /echoBack\n");
    printf("==================================================\n");

    return server;
}

void stopWebserver(httpd_handle_t server){
  if (server) {
    httpd_stop(server);
  }
}
