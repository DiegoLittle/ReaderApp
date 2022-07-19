import { useMediaQuery } from 'usehooks-ts'


export function get_device_size(){
    var device_size
    const isLG = useMediaQuery('(min-width: 1024px)')
    const isMD = useMediaQuery('(min-width: 768px)')
    const isXL = useMediaQuery('(min-width: 1280px)')
    const isSM = useMediaQuery('(min-width: 640px)')
    if(isXL){
      device_size = "xl"
    }
    else if(isLG){
      device_size = "lg"
    }
    else if(isMD){
      device_size = "md"
    }
    else if(isSM){
      device_size = "sm"
    }
    else{
      device_size = "xs"
    }
    return device_size
  }