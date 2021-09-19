
let last_selected_id = 0;

function m_over(){
    let thumnails = document.getElementsByClassName("thumnail");
    for(let i=0, len=thumnails.length; i<len; i++){
        thumnails[i].style.opacity="1";
        thumnails[i].style.zIndex="1";
    }
}

function m_out(){
    let thumnails = document.getElementsByClassName("thumnail");
    for(let i=0, len=thumnails.length; i<len; i++)
        if( thumnails[i].id !== last_selected_id ){
            thumnails[i].style.opacity="0.4";
            thumnails[i].style.zIndex="0";
        }
}


