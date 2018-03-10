 document.getElementById("showurl").onclick = function() {

 		chrome.tabs.getSelected(null, function(tab) { 
 			document.getElementById("currentURL").innerHTML = tab.url;	
 			var PageURL = {
 				"url" : tab.url,
 				"query" : document.getElementById("query").value
 				};
 				
 			$.ajax({
     			type: 'POST',
     			url: '/GetandParse',
     			data: PageURL,
     			dataType: 'json',
     			success: function(data) { 
                   if(data.error){
 					  document.getElementById("returnmsg").innerHTML = data.error;
 				   } else {
 					  document.getElementById("returnmsg").innerHTML = data.return_url;
 				   }
     			},
     			error: function(xhr, type) {
     			}
 			});
 		});
 		
 		event.preventDefault();
 };

//$(document).ready(function() {
//
//	$('form').on('submit', function(event){
//	
//		chrome.tabs.getSelected(null, function(tab) { 
//			document.getElementById("currentURL").innerHTML = tab.url;	
//			var PageURL = {
//				"url" : tab.url,
//				"query" : document.getElementById("query").value
//				};
//				
//			$.ajax({
//    			type: 'POST',
//    			url: '/GetandParse',
//    			data: PageURL,
//			})
//			.done(function(data) {
//				
////				if(data.error){
////					document.getElementById("returnmsg").innerHTML = data.error;
////				} else {
////					document.getElementById("returnmsg").innerHTML = data.return_url;
////				}
//                document.getElementById("returnmsg").innerHTML = "Error";
//			
//			});
//		});
//        event.preventDefault();
//	});
//	
//
//});