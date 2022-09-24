#include "esp_http_server.h"
#include <Arduino.h>
#include <ArduinoJson.h>
#include "esp_camera.h"

extern bool needToReset;
extern String camId;
extern String camQuality;
extern String camRotate;
extern unsigned long intervalFrameMillis;
extern String clientIp;
extern String clientPort;

const int payloadLength = 150;

camera_fb_t* takePhoto();
void saveVariables();

  /*
  *  GET /isAlive
  */
  esp_err_t handler_get_is_alive(httpd_req_t *req){
    Serial.println("Request arrived to serve \"GET /isAlive");
    const char resp[] = "{'status': 'OK'}";
    esp_err_t res = httpd_resp_send(req, resp, strlen(resp));
    printf("   Request \"GET /isAlive\" was served\n\n", "");    
    return res;
  }

  /*
  * GET /capture
  */
  esp_err_t handler_get_capture(httpd_req_t *req){
    esp_err_t res = ESP_OK;

    Serial.println("Request arrived to serve \"GET /capture");

    camera_fb_t * fb = NULL;
    fb = takePhoto();
  
    if (!fb) {
      Serial.println("   !!! Camera CAPTUE failed !!!\n");
      httpd_resp_send_500(req);
      return ESP_FAIL;
    }

    // Response Header
    httpd_resp_set_type(req, "image/jpeg");
    httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");

    size_t out_len, out_width, out_height;
    uint8_t * out_buf;
    bool s;

    size_t fb_len = 0;
    fb_len = fb->len;
  
    res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
    
    printf("   Request \"GET /capture\" was served - JPG: %uB\n\n", (uint32_t)(fb_len));    
  
    return res;
  }

  /*
  *  GET /configure
  */
  esp_err_t handler_get_configure(httpd_req_t *req){
    Serial.println("Request arrived to serve \"GET /configure");
    
    String statusJson = "'status': 'OK'";
    String valueJson = 
    "'value': {'needToReset': '" + String(needToReset) + 
    "', 'camId': '" + camId + 
    "', 'camQuality': '" + camQuality + 
    "', 'camRotate': '" + camRotate + 
    "', 'intervalFrameMillis': '" + intervalFrameMillis + 
    "', 'clientIp': '" + clientIp + 
    "', 'clientPort': '" + clientPort +     
    "'}";
   
    String allJson = "{" + statusJson + ", " + valueJson + "}";
    int str_len = allJson.length() + 1;

    char resp[str_len];
    allJson.toCharArray(resp, str_len);
    
    esp_err_t res = httpd_resp_send(req, resp, strlen(resp));
    printf("   Request \"GET /configure\" was served\n\n", "");    
    return res;
  }
  
  /*
  * POST /configure
  * 
  * The POST request will ended with "Connection reset by peer" error because before it returns
  * with result (OK) it will ESP.reset()
  * 
  * body{
  *  camId: "1",
  *  camQuality: "HD",      //96X96,QQVGA,QCIF,HQVGA,240X240,QVGA,CIF,HVGA,VGA,SVGA,XGA,HD,SXGA,UXGA
  *  camRotate: "1",        //1, 2, 3, 0
  *  intervalFrame: "20000" //in ms
  *  clientIp: "192.168.0.104",
  *  clientPort: "80"
  * }
  */
esp_err_t handler_post_configure(httpd_req_t *req){
  //esp_err_t res = ESP_OK;
  char resp[] = "{'status': 'OK'}";

  Serial.println("Request arrived to serve \"POST /configure");

  /* Destination buffer for content of HTTP POST request.
   * httpd_req_recv() accepts char* only, but content could
   * as well be any binary data (needs type casting).
   * In case of string data, null termination will be absent, and
   * content length would give length of string */
  char payload[payloadLength];

  /* Truncate if content length larger than the buffer */
  size_t recv_size = min(req->content_len, sizeof(payload));

  int ret = httpd_req_recv(req, payload, recv_size);

Serial.print("   Payload: ");
Serial.println(payload);
  
  if (ret <= 0) {  /* 0 return value indicates connection closed */
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

  //pharse the parameters (string->json)
  DynamicJsonDocument doc(payloadLength);
  DeserializationError error = deserializeJson(doc, payload);
  if (error) {
    Serial.println(F("   !!! Wrong parameter was sent !!!"));      
    strcpy(resp,"{'status': 'ERROR'}");
  }else{

    const char* myCamId = doc["camId"];
    if (myCamId){
      camId = String(myCamId);
    }

    // 96X96,QQVGA,QCIF,HQVGA,240X240,QVGA,CIF,HVGA,VGA,SVGA,XGA,HD,SXGA,UXGA
    const char* myCamQuality = doc["camQuality"];
    if (myCamQuality){
      camQuality = String(myCamQuality);
   }

    // 1, 2, 3, 0
    const char* myCamRotate = doc["camRotate"];
    if (myCamRotate){
      camRotate = String(myCamRotate);
    }

    const char* myIntervalFrame = doc["intervalFrame"];
    if (myIntervalFrame){
      intervalFrameMillis = strtoul(myIntervalFrame, NULL, 0);
    }

    const char* myClientIp = doc["clientIp"];
    if (myClientIp){
      clientIp = String(myClientIp);
    }

    const char* myClientPort = doc["clientPort"];
    if (myClientPort){
      clientPort = String(myClientPort);
    }

    needToReset = true;
    saveVariables();
  }

  esp_err_t res = httpd_resp_send(req, resp, strlen(resp));
  printf("   Request \"POST /configure\" was served\n\n", "");    
  return res;
}

httpd_handle_t startWebServer(){

    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    httpd_handle_t server = NULL;
    
    httpd_uri_t uri_get_is_alive = {
        .uri       = "/isAlive",
        .method    = HTTP_GET,
        .handler   = handler_get_is_alive,
        .user_ctx  = NULL
    };

    httpd_uri_t uri_get_capture = {
        .uri       = "/capture",
        .method    = HTTP_GET,
        .handler   = handler_get_capture,
        .user_ctx  = NULL
    };

    httpd_uri_t uri_get_configure = {
        .uri       = "/configure",
        .method    = HTTP_GET,
        .handler   = handler_get_configure,
        .user_ctx  = NULL
    };
    
    httpd_uri_t uri_post_configure = {
        .uri       = "/configure",
        .method    = HTTP_POST,
        .handler   = handler_post_configure,
        .user_ctx  = NULL
    };
    
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_register_uri_handler(server, &uri_get_is_alive);
        httpd_register_uri_handler(server, &uri_get_capture);
        httpd_register_uri_handler(server, &uri_get_configure);
        httpd_register_uri_handler(server, &uri_post_configure);
    }

    printf("==================================================\n");
    printf("Starting web server on port: '%d'\n", config.server_port);
    printf("         %s", "GET /isAlive\n");
    printf("         %s", "GET /capture\n");
    printf("         %s", "GET /configure\n");
    printf("         %s", "POST /configure\n");
    printf("==================================================\n");

    return server;
}

void stopWebserver(httpd_handle_t server){
  if (server) {
    httpd_stop(server);
  }
}
