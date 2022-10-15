double getAvgTemp(){
  double avgTemp = NULL;
  if(avgBmpTemp != NULL && avgDhtTemp != NULL){
    avgTemp = (avgBmpTemp + avgDhtTemp) / 2;
  }else if(avgBmpTemp != NULL){
    avgTemp = avgBmpTemp;
  }else if(avgDhtTemp != NULL){
    avgTemp = avgDhtTemp;
  }
  return avgTemp;
}
