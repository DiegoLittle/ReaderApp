let changeColor = document.getElementById("changeColor");
let titleField = document.getElementById('title');
let saveButton = document.getElementById('saveButton');

chrome.storage.sync.get("color", ({ color }) => {
  changeColor.style.backgroundColor = color;
});


// document.title = "Hello World";
document.addEventListener('DOMContentLoaded', async function () {

  

  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  titleField.value = tab.title;
//   const url = new URL('https://read.synesthesia.ai');
    
// //   const cookies = await chrome.cookies.getAll({
// //     domain:url.hostname
// //   });
// //   // console.log(cookies)
// //   // const myHeaders = new Headers();
// //   const opts = {
// //     headers: {
// //         cookie: '__Host-next-auth.csrf-token=93f4c38c73f5f19adcba535c7debcbe6b9e8278eb6561b98529b40e0586159c1%7C9118ccbbd6dc5eff834d193743e7295b29c77caede2788a9b9587be952cf89f6; __Secure-next-auth.callback-url=https%3A%2F%2Fread.synesthesia.ai; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..xulNDSYeqKiM7n1Z.MizQhRWLsEU-kfPYvTcm7VsqqOyIwBeRGmM7ZEih3i8Vc3pntltimJFrlNQ531PWHKDoF9YsCQPuLTG_IfGaDQeM2gkj4a7nkfVLpeiZvjV2LS5tWS_7JRXz2O2IqV6PEfTnhrIF5-VxD1CVDmLFoUBuP0BTl1pAOYni2GjWqSaUs1th_x29FZZvpdcLTTEAH3GfOVnrFJU9Y6COzdaI0i91nSC-YoKVIzWPJ5L1M6NDA5DQ8sgQCrJRQA-aMaU3Yl5Q.hIRhGM8L0nh6kjo2szjoFw'
// //     }
// // };
// //   let res = await fetch('https://read.synesthesia.ai/api/auth/session',opts)
// //   let data = await res.json()

});

// When the button is clicked, inject setPageBackgroundColor into current page
saveButton.addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    console.log(tab.title)
    console.log(tab.url)
  
    let add_res = await fetch('https://read.synesthesia.ai/api/add_bookmark?url='+tab.url+'&title='+tab.title)
    let add_data = await add_res.json()
    console.log(add_data)
    saveButton.innerText = "Saved"
    // console.log("Hello")
    // chrome.runtime.sendMessage('get-user-data', (response) => {
    //   // 3. Got an asynchronous response with the data from the background
    //   console.log('received user data', response);
    //   // initializeUI(response);
    // });
    // let res = await fetch("https://jsonplaceholder.typicode.com/todos/1")
    // let data = await res.json()
    // // console.log(data)
    // changeColor.innerText = JSON.stringify(cookies)
  //   fetch('http://localhost:8000/test',{
  //   method: 'POST',
  //   headers: {
  //     'Content-Type':'application/json',
  //     'Accept': 'application/json'
  //   },
  //   body:JSON.stringify({
  //     "title":tab.title,
  //     "url":tab.url,
  //   })
  // });
  
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: setPageBackgroundColor,
    });
  });
  
  // The body of this function will be executed as a content script inside the
  // current page
  function setPageBackgroundColor() {
    chrome.storage.sync.get("color", ({ color }) => {
      // document.body.style.backgroundColor = color;


  });
  }

