#define FILE_NAME "/control_config.json"
#define BUFF_SIZE 1024

// --- Config file ---
//String essid;
//String password;
//String webserver_ip;
//String webserver_path_info_timestamp;
//String webserver_path_cam_register;
//String webserver_path_info_is_alive;
//
//String cam_id;
////int lamp_gpio;
////int pump_gpio;
//int led_status_gpio;
//int led_status_inverse;
//int register_interval_sec;
//int reset_hours;
// -------------------

bool loadConfig(){
  File configFile = SPIFFS.open(FILE_NAME, "r");
  if( !configFile){
    Serial.println("Failed to open config file for reading");
    return false;
  }

  size_t size = configFile.size();
  if(size > BUFF_SIZE){
    configFile.close();
    Serial.println("config file size is too large");
    return false;
  }

  std::unique_ptr<char[]> buf(new char[size]);
  configFile.readBytes(buf.get(), size);
  Serial.println(buf.get());

  DynamicJsonDocument json(BUFF_SIZE);
  DeserializationError error = deserializeJson(json, buf.get());

  configFile.close();

  if(error){
    Serial.println("Failed to parse config file");
    return false;
  }

  essid = (String)(const char*)json["central-ap"]["essid"];
  password = (String)(const char*)json["central-ap"]["password"];
  webserver_ip = (const char*)json["central-ap"]["webserver-ip"];
  webserver_path_info_timestamp = (const char*)json["central-ap"]["webserver-path-info-timestamp"];
  webserver_path_cam_register = (const char*)json["central-ap"]["webserver-path-cam-register"];
  webserver_path_info_is_alive = (const char*)json["central-ap"]["webserver-path-info-is-alive"];

  cam_id = (const char*)json["sensor-sta"]["cam-id"];
  led_status_gpio = json["sensor-sta"]["led-status-gpio"];
  led_status_inverse = json["sensor-sta"]["led-status-inverse"];
  register_interval_sec = json["sensor-sta"]["register-interval-sec"];
  reset_hours = json["sensor-sta"]["reset-hours"];
  
  // ---

  Serial.print("central-ap.essid = ");
  Serial.println(essid);

  Serial.print("central-ap.password = ");
  Serial.println(password);

  Serial.print("central-ap.webserver-ip = ");
  Serial.println(webserver_ip);
  
  Serial.print("central-ap.webserver-path-info-timestamp = ");
  Serial.println(webserver_path_info_timestamp);
  
  Serial.print("central-ap.webserver-path-cam-register = ");
  Serial.println(webserver_path_cam_register);
  
//  Serial.print("central-ap.webserver-path-pump-register = ");
//  Serial.println(webserver_path_pump_register);

  Serial.print("central-ap.webserver-path-info-is-alive = ");
  Serial.println(webserver_path_info_is_alive);

  Serial.print("sensor-sta.cam-id = ");
  Serial.println(cam_id);

//  Serial.print("sensor-sta.lamp-gpio = ");
//  Serial.println(lamp_gpio);

//  Serial.print("sensor-sta.pump-gpio = ");
//  Serial.println(pump_gpio);
  
  Serial.print("sensor-sta.led-status-gpio = ");
  Serial.println(led_status_gpio);
  
  Serial.print("sensor-sta.led-status-inverse = ");
  Serial.println(led_status_inverse);
  
  Serial.print("sensor-sta.register-interval-sec = ");
  Serial.println(register_interval_sec);

  Serial.print("sensor-sta.reset-hours = ");
  Serial.println(reset_hours);

  return true;
}
