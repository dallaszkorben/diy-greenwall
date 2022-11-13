double getAvgTemp(double temp1, double temp2){
  double avgTemp = NULL;

  if(temp1 != NULL && temp2 != NULL){
    avgTemp = (temp1 + temp2) / 2;
  }else if(temp1 != NULL){
    avgTemp = temp1;
  }else if(temp2 != NULL){
    avgTemp = temp2;
  }
  
//  if(avgBmpTemp != NULL && avgDhtTemp != NULL){
//    avgTemp = (avgBmpTemp + avgDhtTemp) / 2;
//  }else if(avgBmpTemp != NULL){
//    avgTemp = avgBmpTemp;
//  }else if(avgDhtTemp != NULL){
//    avgTemp = avgDhtTemp;
//  }
  
  return avgTemp;
}

boolean isBoolean(String str) {
    unsigned int stringLength = str.length();
 
    if (stringLength == 0) {
        return false;
    }

    str.toLowerCase();
    if(str.equals("true")){
      return true;
    }
    else if (str.equals("t")){
      return true;
    }
    else if (str.equals("1")){
      return true;
    }
    else if (str.equals("0")){
      return true;
    }
    else if (str.equals("false")){
      return true;
    }
    else if (str.equals("f")){
      return true;
    }
    else {
      return false;
    }
}

boolean isInteger(String str) {
    unsigned int stringLength = str.length();
 
    if (stringLength == 0) {
        return false;
    }
  
    for(unsigned int i = 0; i < stringLength; ++i) {
      
        if (isDigit(str.charAt(i))) {
            continue;
        }else if ( i == 0 && str.charAt(0) == '-') {
          continue;
        }
 
        return false;
    }
    return true;
}

boolean isDecimal(String str) {
    unsigned int stringLength = str.length();
 
    if (stringLength == 0) {
        return false;
    }
 
    boolean seenDecimal = false;
 
    for(unsigned int i = 0; i < stringLength; ++i) {
      
        if (isDigit(str.charAt(i))) {
            continue;
        }else if ( i == 0 && str.charAt(0) == '-') {
          continue;
        }
 
        if (str.charAt(i) == '.') {
            if (seenDecimal) {
                return false;
            }
            seenDecimal = true;
            continue;
        }
        return false;
    }
    return true;
}


static bool ToBoolean(String value){
  value.toLowerCase();
  if(value.equals("true")){
    return true;
  }
  else if (value.equals("t")){
    return true;
  }
  else if (value.equals("1")){
    return true;
  }
  else if (value.equals("0")){
    return false;
  }
  else if (value.equals("false")){
    return false;
  }
  else if (value.equals("f")){
    return false;
  }
  else {
    return false;
  }
}
