document.addEventListener('DOMContentLoaded',function(){

    console.log("1st")
    fetch("/loadbox")
    .then(response => response.json())
    .then(messages =>{
        messages.forEach(function(message){
            let mysection = document.createElement('div') ;
            let content = `<a href="#" class="posta"> 
            <img src="${message.sender_image}" class="rounded-circle" >
            <h4>${message.sender}<span style="font-size:12px;float:right;margin-top:10px;margin-right:10px;"> at     ${message.timestamp}</span> </h4>
            <p style="display:inline;" >${message.content}</p></a>`
            mysection.innerHTML = content ;
            mysection.href = '#';
            mysection.setAttribute('class','msec'); ;
            document.querySelector('#body_inbox').append(mysection) ;
            //console.log(message);
            if(!message.read){
                mysection.style.backgroundColor ="#D3D3D3";
            }else{
                mysection.style.backgroundColor ="#808080"
            }
            
            mysection.onclick = function(section){
                fetch(`/load/${message.id}`,{
                    method:'PUT',
                    body:JSON.stringify({
                        read:true
                    })

                })
                .then(response  => response.json())
                .then(data =>{
                    //console.log(data);
                })
                this.style.backgroundColor = "#808080";



                fetch(`/load/${message.id}`)
                .then(response => response.json())
                .then(messages_box =>{
                //console.log(messages_box);
                document.querySelector('.right_div').innerHTML = '';
                document.querySelector('.right_div').style.display = "block";
                document.querySelector('.right_div').innerHTML = `<div class="photo_chat"style="height:80px;border:1px solid black;display:block;">
                <img src="${message.sender_image}" class="rounded-circle" style="width:60px;height:60px;"><h4 style="margin-top:10px;">${message.sender}</h4>
                <p style="float:right;position:relative;bottom:40px;right:20px;">${message.sender_email}</p></div>`
                messages_box.forEach(function(message_box){
                    message_square=document.createElement('div');
                    message_square.setAttribute('class','message_square') ;
                    if (message_box.sender === message.receiver){
                        message_square.innerHTML = `<p style="float:right;color:white;backgroundColor:blue;margin-right:50px;margin-top:10px;" >${message_box.content}</p>`;
                        message_square.style.backgroundColor = "#006AFF";
                        message_square.style.float = "right";
                        
                    }else{
                        message_square.innerHTML = `<p style="float:left;backgroundColor:red;margin-left:50px;margin-top:10px;" >${message_box.content}</p>`;
                        message_square.style.backgroundColor = "#F5F5F5";
                        message_square.style.float = "left";
                    }
                    document.querySelector('.right_div').append(message_square) ;
                })
                input=document.createElement('div');
                input.setAttribute('class','input')
                input.innerHTML =`<div class="m-form" >
                <form id="inbox_form" class="form-control">
                <input class="msj-i" required type="text" placeholder="Start a new message"></input>
                <input type="submit" value="Send" class="msj-s"></input>
                </form> </div>`;
                document.querySelector('.right_div').append(input) ;
                document.querySelector('#inbox_form').onsubmit = function(){
                    let message_sender= `${message.sender}` ;
                    let input1  = document.querySelector('.msj-i').value ;
                    fetch('/directmessages',{
                        method:'POST',
                        body:JSON.stringify({
                            message_sender:message_sender,
                            input:input1
                        })
                    })
                    .then(response => response.json())
                    .then(data =>{
                        console.log(data.input);
                        message_square=document.createElement('div');
                        message_square.setAttribute('class','message_square') ;
                    
                        message_square.innerHTML = `<p style="float:right;color:white;backgroundColor:blue;margin-right:50px;margin-top:10px;" >${data.input}</p>`;
                        message_square.style.backgroundColor = "#006AFF";
                        message_square.style.float = "right";
                        
                        document.querySelector('.right_div').insertBefore(message_square, document.querySelector('.input'));
                    // document.querySelector('.right_div').append(message_square) ;
                    

                    })

                };
            })
            }
            

        });
        
    })
    //console.log('finshed') ;

});