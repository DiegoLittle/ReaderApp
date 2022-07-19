// background.js
let color = '#3aa757';

const test = {
  username: 'demo-user'
};



async function getCurrentTab() {
  let queryOptions = { active: true, currentWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

// let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
// console.log("tab", tab);

// chrome.action.onClicked.addListener((tab) => {
//   chrome.scripting.executeScript({
//     target: { tabId: tab.id },
//     files: ['content-script.js']
//   });
// });


chrome.runtime.onMessage.addListener(async(message, sender, sendResponse) => {
  // 2. A page requested user data, respond with a copy of `user`
  console.log("message", message)
  
  if (message === 'get-user-data') {
    
//     const url = new URL('https://read.synesthesia.ai');
    
//   const cookies = await chrome.cookies.getAll({
//     domain:url.hostname
//   });
//   // console.log(cookies)
//   // const myHeaders = new Headers();
//   const opts = {
//     headers: {
//         cookie: '__Host-next-auth.csrf-token=93f4c38c73f5f19adcba535c7debcbe6b9e8278eb6561b98529b40e0586159c1%7C9118ccbbd6dc5eff834d193743e7295b29c77caede2788a9b9587be952cf89f6; __Secure-next-auth.callback-url=https%3A%2F%2Fread.synesthesia.ai; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..xulNDSYeqKiM7n1Z.MizQhRWLsEU-kfPYvTcm7VsqqOyIwBeRGmM7ZEih3i8Vc3pntltimJFrlNQ531PWHKDoF9YsCQPuLTG_IfGaDQeM2gkj4a7nkfVLpeiZvjV2LS5tWS_7JRXz2O2IqV6PEfTnhrIF5-VxD1CVDmLFoUBuP0BTl1pAOYni2GjWqSaUs1th_x29FZZvpdcLTTEAH3GfOVnrFJU9Y6COzdaI0i91nSC-YoKVIzWPJ5L1M6NDA5DQ8sgQCrJRQA-aMaU3Yl5Q.hIRhGM8L0nh6kjo2szjoFw'
//     }
// };
//   let res = await fetch('https://read.synesthesia.ai/api/auth/session',opts)
//   let data = await res.json()
//   console.log(data)
    await sendResponse(data);
  }
});


function activeListener(){
  chrome.tabs.onActivated.addListener((activeInfo)=>{
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
      let url = tabs[0].url;
      console.log("Debugging onActive :(")
      console.log(tabs[0])
      console.log(url.includes("example.com"))

      if(url.includes("example.com")){
          chrome.tabs.remove(tabs[0].id);
      chrome.tabs.create({
        url:"https://google.com"
      })
    }


  });

  }
  )
}

chrome.runtime.onInstalled.addListener(async () => {

  console.log("Run time installed")

  chrome.storage.sync.set({ color });
  console.log('Default background color set to %cgreen', `color: ${color}`);

  chrome.webNavigation.onBeforeNavigate.addListener((e)=>{
    console.log("Hello World")
    // console.log(e)
    // console.log(Object.keys(e).includes("url"))
    if(Object.keys(e).includes("url")){
      
    console.log(e.url)
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {

      console.log(e.url.includes("arxiv.org/pdf/"))
      if(e.url.includes("arxiv.org/pdf/")){
        let arxiv_id = e.url.split("arxiv.org/pdf/")[e.url.split("arxiv.org/pdf/").length-1].replace(".pdf","")
          chrome.tabs.remove(tabs[0].id);
      chrome.tabs.create({
        url: "https://read.synesthesia.ai/read/"+arxiv_id
      })
    }


  });
}

  }
  )
});
