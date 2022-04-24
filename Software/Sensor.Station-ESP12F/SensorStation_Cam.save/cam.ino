#include "Base64.h"

bool configureCam(){

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  config.pixel_format = PIXFORMAT_JPEG;

  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return false;
  }
  return true;
}

// Capture Photo
camera_fb_t* capturePhoto( void ) {
    camera_fb_t * fb = NULL; // pointer

    // Take a photo with the camera
    Serial.println("Taking a photo...");

    fb = esp_camera_fb_get();
    if (fb) {
      esp_camera_fb_return(fb);
      Serial.println("Photo was taken");
    }else{
      Serial.println("Failed to takephoto...");
    }



/*    uint8_t *fbBuf = fb->buf;
    size_t fbLen = fb->len;    
    for (size_t n=0; n<fbLen; n=n+1024) {
      if (n+1024 < fbLen) {
        client.write(fbBuf, 1024);
        fbBuf += 1024;
      }
      else if (fbLen%1024>0) {
        size_t remainder = fbLen%1024;
        client.write(fbBuf, remainder);
      }
    }   */

/*
    char *input = (char *)fb->buf;
    char output[base64_enc_len(3)];
    String imageFile = "";
    for (int i = 0; i < fb->len; i++) {
      base64_encode(output, (input++), 3);
      if (i % 3 == 0) imageFile += urlencode(String(output));
    }
    //String Data = myFilename + mimeType + myImage;    
    Serial.println(imageFile);
*/
    
    return fb;
}
