
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

function vote_gage_event(vote_average){
    vote_average = vote_average*10;
    if ( vote_average < 50.0 )
        document.getElementById("vote_gage_bar").style.backgroundColor = "red";
    else
        document.getElementById("vote_gage_bar").style.backgroundColor = "rgb(47, 255, 28)";
    vote_average = String(vote_average)+'%';
    
    document.getElementById("vote_gage_bar").style.width = vote_average;
};
window.onload = vote_gage_event("{{ selected_movie.vote_average }}");
