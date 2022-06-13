#include "esp_http_server.h"
#include <Arduino.h>
#include <ArduinoJson.h>
#include "esp_camera.h"

/*
typedef struct {
        httpd_req_t *req;
        size_t len;
} jpg_chunking_t;

static size_t jpg_encode_stream(void * arg, size_t index, const void* data, size_t len){
    jpg_chunking_t *j = (jpg_chunking_t *)arg;
    if(!index){
        j->len = 0;
    }
    if(httpd_resp_send_chunk(j->req, (const char *)data, len) != ESP_OK){
        return 0;
    }
    j->len += len;
    return len;
}
*/

camera_fb_t* takePhoto();

/*
 *  GET /isAlive
 */
esp_err_t handler_is_alive(httpd_req_t *req){
  const char resp[] = "{'status': 'OK'}";
  esp_err_t res = httpd_resp_send(req, resp, strlen(resp));
  printf("   Request \"GET /isAlive\" was served\n", "");    
  return res;
}

/*
 * GET /capture
 */
esp_err_t handler_capture(httpd_req_t *req){
  esp_err_t res = ESP_OK;

  camera_fb_t * fb = NULL;
  fb = takePhoto();
  
  if (!fb) {
    Serial.println("!!! Camera CAPTUE failed !!!");
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
/*  jpg_chunking_t jchunk = {req, 0};
  res = frame2jpg_cb(fb, 80, jpg_encode_stream, &jchunk)?ESP_OK:ESP_FAIL;
  httpd_resp_send_chunk(req, NULL, 0);
  fb_len = jchunk.len;
*/
    
  printf("   Request \"GET /capture\" was served - JPG: %uB\n", (uint32_t)(fb_len));    
  
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

    httpd_uri_t uri_get_capture = {
        .uri       = "/capture",
        .method    = HTTP_GET,
        .handler   = handler_capture,
        .user_ctx  = NULL
    };
    
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_register_uri_handler(server, &uri_get_is_alive);
        httpd_register_uri_handler(server, &uri_get_capture);
    }

    printf("==================================================\n");
    printf("Starting web server on port: '%d'\n", config.server_port);
    printf("         %s", "GET /isAlive\n");
    printf("         %s", "GET /capture\n");
    printf("==================================================\n");

    return server;
}

void stopWebserver(httpd_handle_t server){
  if (server) {
    httpd_stop(server);
  }
}
