// On adding a new senate member
$(document).ready(function() {
    
});

//AJAX for adding the new senate member on the list
function upload_minutes() {
    
};

// //on deleting the senate members
// $(document).ready(function() {
//     $("#minute_list").on('click', 'a[id^=remove-minute-]', function(){
//         //alert($(this).attr('id').split('-')[2]);
//         var meeting_id = $(this).attr('id').split('-')[2];
//         delete_minutes(meeting_id);
//     });
// });

// // AJAX for deleting
// function delete_minutes(meeting_id){
//     if (confirm('Are you sure you want to remove this senate from the list?')==true){
//         $.ajax({
//             url : "deleteMinute/"+meeting_id, // the endpoint
//             type : "DELETE", // http method
//             data : { meeting_id : meeting_id }, // data sent with the delete request
//             success : function(data) {
//               $('#minute-'+meeting_id).hide(); // hide the post on success
//               alert("minute removed");
//             },
//             error : function(xhr,errmsg,err) {
//                 alert("Something went wrong");
//             }
//         });
//     } else {
//         return false;
//     }
// };
