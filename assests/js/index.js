search=document.getElementById('search')
search.addEventListener('keyup',searching)
function searching(e){
 convert=e.target.value.toLowerCase()
 items=document.getElementsByClassName('search')
 tit=document.getElementsByClassName('titles')
 for(let i=0;i<tit.length;i++){
     console.log(tit[0])
    if(tit[i].innerText.toLowerCase().indexOf(convert)!=-1){
        items[i].style.display='block'
    }
    else{
        items[i].style.display='none'
    }
 }
}