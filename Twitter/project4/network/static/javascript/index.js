document.addEventListener('DOMContentLoaded',showMessages)
document.addEventListener('DOMContentLoaded', showDelete);
document.addEventListener('DOMContentLoaded',alertMessage)
document.addEventListener('DOMContentLoaded', showFollowings)
document.addEventListener('DOMContentLoaded', showFollowers)
document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('.like').forEach(function(button){
        button.onclick = function(){
            fetch('/like',{
                method:"PUT",
                body:JSON.stringify({
                    like:true ,
                    post_id:button.dataset.postid
                })
            })
            .then(response => response.json())
            .then(data =>{
                if(data.error){
                    console.log(`${data.error}`);
                }else{
                    console.log(data.likes_count);
                }

                like_count_in_post = document.querySelector(`#likes${button.dataset.postid}`).innerHTML ;
                like_real = data.likes_count ;
                // console.log(like_count_in_post);
                // console.log(like_real);
                if (parseInt(like_count_in_post) < parseInt(like_real)){
                    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height:20px;width:23px;" viewBox="0 0 512 512"><path d="M466.27 286.69C475.04 271.84 480 256 480 236.85c0-44.015-37.218-85.58-85.82-85.58H357.7c4.92-12.81 8.85-28.13 8.85-46.54C366.55 31.936 328.86 0 271.28 0c-61.607 0-58.093 94.933-71.76 108.6-22.747 22.747-49.615 66.447-68.76 83.4H32c-17.673 0-32 14.327-32 32v240c0 17.673 14.327 32 32 32h64c14.893 0 27.408-10.174 30.978-23.95 44.509 1.001 75.06 39.94 177.802 39.94 7.22 0 15.22.01 22.22.01 77.117 0 111.986-39.423 112.94-95.33 13.319-18.425 20.299-43.122 17.34-66.99 9.854-18.452 13.664-40.343 8.99-62.99zm-61.75 53.83c12.56 21.13 1.26 49.41-13.94 57.57 7.7 48.78-17.608 65.9-53.12 65.9h-37.82c-71.639 0-118.029-37.82-171.64-37.82V240h10.92c28.36 0 67.98-70.89 94.54-97.46 28.36-28.36 18.91-75.63 37.82-94.54 47.27 0 47.27 32.98 47.27 56.73 0 39.17-28.36 56.72-28.36 94.54h103.99c21.11 0 37.73 18.91 37.82 37.82.09 18.9-12.82 37.81-22.27 37.81 13.489 14.555 16.371 45.236-5.21 65.62zM88 432c0 13.255-10.745 24-24 24s-24-10.745-24-24 10.745-24 24-24 24 10.745 24 24z"/></svg> Unlike';
                    button.style="width: 32.65%; display: inline-block; background-color:rgba(29,161,242,0.3);";
                }else{
                    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height:20px;width:23px;" viewBox="0 0 512 512"><path d="M466.27 286.69C475.04 271.84 480 256 480 236.85c0-44.015-37.218-85.58-85.82-85.58H357.7c4.92-12.81 8.85-28.13 8.85-46.54C366.55 31.936 328.86 0 271.28 0c-61.607 0-58.093 94.933-71.76 108.6-22.747 22.747-49.615 66.447-68.76 83.4H32c-17.673 0-32 14.327-32 32v240c0 17.673 14.327 32 32 32h64c14.893 0 27.408-10.174 30.978-23.95 44.509 1.001 75.06 39.94 177.802 39.94 7.22 0 15.22.01 22.22.01 77.117 0 111.986-39.423 112.94-95.33 13.319-18.425 20.299-43.122 17.34-66.99 9.854-18.452 13.664-40.343 8.99-62.99zm-61.75 53.83c12.56 21.13 1.26 49.41-13.94 57.57 7.7 48.78-17.608 65.9-53.12 65.9h-37.82c-71.639 0-118.029-37.82-171.64-37.82V240h10.92c28.36 0 67.98-70.89 94.54-97.46 28.36-28.36 18.91-75.63 37.82-94.54 47.27 0 47.27 32.98 47.27 56.73 0 39.17-28.36 56.72-28.36 94.54h103.99c21.11 0 37.73 18.91 37.82 37.82.09 18.9-12.82 37.81-22.27 37.81 13.489 14.555 16.371 45.236-5.21 65.62zM88 432c0 13.255-10.745 24-24 24s-24-10.745-24-24 10.745-24 24-24 24 10.745 24 24z"/></svg> Like' ;
                    button.style="width: 32.65%; display: inline-block;background-color:white;";

                }
                document.querySelector(`#likes${button.dataset.postid}`).innerHTML = like_real ;
            })
        }
    });
    
    document.querySelectorAll('.edit').forEach(function(button){
        button.onclick = function(){
            post_id = button.dataset.postid ;
            button.style.display = "none";
            // console.log(post_id); 
            content = document.querySelector(`#content${post_id}`)
            // console.log(content.innerHTML);
            content.innerHTML =  `
            <div style="position:relative;top:80px;right:60px;width:710px;height:auto;">
            <form id="textarea-edit-post">
            <textarea  class="txt_tweet"
            id = "txtArea_edit"
            cols="20" 
            rows="4"
            onkeyup="if (this.scrollHeight > this.clientHeight) this.style.height = this.scrollHeight + 'px';"
            style="position: relative;absoverflow:hidden; transition: height 0.2s ease-out;opacity:1;border:1px solid lightgrey;"
            placeholder="What's on your mind">${content.innerHTML}</textarea> 
            <input type="submit" class="btn btn-primary post-submit" style="position:relative;bottom:180px;left:23px;" value="Save"/></form> 
            
            </div> `;

        document.querySelector('#textarea-edit-post').onsubmit = function(){
            edit_content = document.querySelector('#txtArea_edit').value ;
            console.log(edit_content);

            fetch('/postedit',{
                method : 'PUT',
                body : JSON.stringify({"content":edit_content ,
                "post_id":post_id
            
                })
            })
                .then(response => response.json())
                .then(data =>{
                    console.log(data)
                

            })
        }
        
    }
    });


    let unfollowBtn = document.querySelector('#unfollowBtn')
    if (unfollowBtn !== null) {
        unfollowBtn.onmouseover = function () {
            unfollowBtn.value = "Unfollow"
            unfollowBtn.className = "btn following-btn"
            unfollowBtn.style.backgroundColor = "#c90d00"
        }
        unfollowBtn.onmouseout = function () {
            unfollowBtn.value = "Following"
            unfollowBtn.className = "btn following-btn"
            unfollowBtn.style.backgroundColor = "rgba(29,161,242,1.00)"
        }
    }

    



});
function showMessages(){
    document.querySelector('.message_button').addEventListener('click',function(){
        document.querySelector('.msj-content').style.display = 'block';
        console.log('ok')
    });
    document.querySelector('.f-mclose').addEventListener('click',function(){
        document.querySelector('.msj-content').style.display = 'none';
    });
}
function alertMessage(){
    document.querySelector('#msj-send').addEventListener('click',function(){
        alert("Message Sent Succussfully !");
    });
}

function showFollowings(){
    document.querySelector('#fsBtn').addEventListener('click',function(){
        document.querySelector('.fs-modal').style.display = 'block';
    })
    document.querySelector('.fsclose').onclick = function(){
        document.querySelector('.fs-modal').style.display = 'none';
    }
}

function showFollowers() {
    document.querySelector('#fBtn').addEventListener('click', () => {
    document.querySelector('.fg-modal').style.display ='block';
      })
    document.querySelector(".fclose").addEventListener('click',() => {
    document.querySelector('.fg-modal').style.display ='none';
      })
  }

function showDelete () {
    document.querySelectorAll('.delete').forEach(function(button){
        button.onclick = function(){
            post_id = button.dataset.postid ;
            document.querySelector(`#delete${post_id}`).style.display ='block';

            document.querySelector(`#cancel${post_id}`).addEventListener('click', () => {
                document.querySelector(`#delete${post_id}`).style.display ='none';
              });
            
        }
    })
    
   
    
  }
