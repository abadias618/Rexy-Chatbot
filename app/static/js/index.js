/*
Rexy
@author: abd
*/
function send () {
    let usr_input = document.getElementById("user-bubble-input").value; 
    //console.log(document.getElementById("user-bubble-input").value);
    //console.log(document.getElementById("user-bubble"));
    //console.log(document.getElementById("user-bubble").innerHTML);
    //prevent empty messages being sent
    if (usr_input !== "" && /\S/.test(usr_input)) {
        //make the input field -> plain text
        document.getElementById("user-bubble").innerHTML = usr_input;
        document.getElementById("user-bubble").id = "";
        //send message to the server to be processed
        let rexy_response_div = document.createElement("div");
        rexy_response_div.className = "speech-bubble-rexy";
        rexy_response_div.innerHTML = `<i id="spinner" class="fa fa-spinner fa-spin fa-2x"></i>`;
        document.body.appendChild(rexy_response_div);
        let x = submit_message(usr_input).then(submit => {
            //console.log("submit", submit);
            rexy_response_div.innerHTML = submit["rexy_answer"];
            
            let new_div = document.createElement("div");
            new_div.id = "user-bubble";
            new_div.className = "speech-bubble-user";
            new_div.innerHTML = `<input id="user-bubble-input" class="send" type="text">
                                <button class="send-button" onclick="send();">
                                    <i class="fa fa-paper-plane fa-2x"></i>
                                </button>`;
            document.body.appendChild(new_div);
        })
        
    }
    
}
function submit_message(usr_input) {
    var user_request = {
      user_question: usr_input
    };
    return new Promise((resolve, reject) => {
    
        fetch('/post-message', {
          method: "POST",
          mode: "cors",
          credentials: "include",
          body: JSON.stringify(user_request),
          cache: "no-cache",
          headers: new Headers({
            "content-type": "application/json"
          })
        })
        .then(response => response.json())
        .then(response => {
          //console.log("resolve response",response);
          resolve(response);
        })
        .catch(error => {
          console.log("Fetch error: " + error);
          reject(error);
        });
    
    });
    
}
