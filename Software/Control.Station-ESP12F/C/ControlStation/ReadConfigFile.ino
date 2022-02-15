#define FILE_NAME "/control_config.json"
#define BUFF_SIZE 1024

// --- Config file ---
String essid;
String password;
String webserver_ip;
String webserver_path_info_timestamp;
String webserver_path_lamp_register;
String webserver_path_pump_register;

String lamp_id;
int lamp_gpio;
int pump_gpio;
int led_status_gpio;
int led_status_inverse;
int register_interval_sec;
int reset_hours;
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

  StaticJsonBuffer<BUFF_SIZE> jsonBuffer;
  JsonObject& json = jsonBuffer.parseObject(buf.get());

  configFile.close();

  if( !json.success()){
    Serial.println("Failed to parse config file");
    return false;
  }

  essid = String(json["central-ap"]["essid"]);
  password = String(json["central-ap"]["password"]);
  webserver_ip = String(json["central-ap"]["webserver-ip"]);
  webserver_path_info_timestamp = String(json["central-ap"]["webserver-path-info-timestamp"]);
  webserver_path_lamp_register = String(json["central-ap"]["webserver-path-lamp-register"]);
  webserver_path_pump_register = String(json["central-ap"]["webserver-path-pump-register"]);
  
  lamp_id = String(json["control-sta"]["lamp-id"]);
  lamp_gpio = json["control-sta"]["lamp-gpio"];
  pump_gpio = json["control-sta"]["pump-gpio"];
  led_status_gpio = json["control-sta"]["led-status-gpio"];
  led_status_inverse = json["control-sta"]["led-status-inverse"];
  register_interval_sec = json["control-sta"]["register-interval-sec"];
  reset_hours = json["control-sta"]["reset-hours"];

  // ---

  Serial.print("central-ap.essid = ");
  Serial.println(essid);

  Serial.print("central-ap.password = ");
  Serial.println(password);

  Serial.print("central-ap.webserver-ip = ");
  Serial.println(webserver_ip);
  
  Serial.print("central-ap.webserver-path-info-timestamp = ");
  Serial.println(webserver_path_info_timestamp);
  
  Serial.print("central-ap.webserver-path-lamp-register = ");
  Serial.println(webserver_path_lamp_register);
  
  Serial.print("central-ap.webserver-path-pump-register = ");
  Serial.println(webserver_path_pump_register);

  Serial.print("control-sta.lamp-id = ");
  Serial.println(lamp_id);

  Serial.print("control-sta.lamp-gpio = ");
  Serial.println(lamp_gpio);

  Serial.print("control-sta.pump-gpio = ");
  Serial.println(pump_gpio);
  
  Serial.print("control-sta.led-status-gpio = ");
  Serial.println(led_status_gpio);
  
  Serial.print("control-sta.led-status-inverse = ");
  Serial.println(led_status_inverse);
  
  Serial.print("control-sta.register-interval-sec = ");
  Serial.println(register_interval_sec);

  Serial.print("control-sta.reset-hours = ");
  Serial.println(reset_hours);

  return true;
}
