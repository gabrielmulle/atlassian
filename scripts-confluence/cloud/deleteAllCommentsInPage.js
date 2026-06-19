javascript:
var x = document.getElementsByTagName('a');
for(i=0; i<x.length; i++){
    if(x[i].getAttribute('data-test-id') =='comment-delete-link'){
            x[i].click();}}
