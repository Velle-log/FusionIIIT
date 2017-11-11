
$(document).ready(function () {


            $('#attend_table').on('click','#edit_tag',function () {         // if user clicks on edit icon
                var roll=$(this).parents('td').siblings()[2];
                var course_code=$(this).parents('td').siblings()[5];        // fetching attendance details of student

                var present_att=$(this).parents('td').siblings()[7];
                var total_att=$(this).parents('td').siblings()[6];
                $('#attend_form,#student_id').val(roll.innerHTML);
                $('#attend_form,#present_attend').val(present_att.innerHTML);   // filling details in form
                $('#attend_form,#total_attend').val(total_att.innerHTML);

            });

            $('#attend_table').on('click','#del_row',function (event) {         // if user clicks delete trash icon
                event.preventDefault();
                var row_element=$(this).parents('td').parents('tr');
                var roll=$(this).parents('td').siblings()[2];                   // fetching attendance of student
                var course_code=$(this).parents('td').siblings()[5];
                var final_warning=confirm('Are you sure you want to delete this student from the course');  // warning
                if(final_warning==true){                    // if warning accepts
                    $.ajax({
                        url: 'delete_attendance',
                        type: 'GET',
                        data: {                                         // sending request
                            student_id: roll.innerHTML,
                            course_id: course_code.innerHTML
                        },
                        success: function (response) {                      // if delete successful
                            if(response.result==='Success'){
                                alert('data deleted successfully');
                                row_element.detach();
                            }
                            else{
                                alert(response.message);
                            }

                        }
                    });
                }
                else{

                }

            });



            $(document).on('submit','#attend_form',function (event) {           // if user submits attendance form
                event.preventDefault();
                var element=$('#course_id .active');
                var course_code=element.data('course');                         // fetch details from form
                $.ajax({
                    url: 'attendance',
                    type: 'POST',                                               // sending POST request through ajax
                    data: {
                        student_id: $('#student_id').val(),
                        course_id: course_code,
                        present_attend: $('#present_attend').val(),
                        total_attend: $('#total_attend').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (response) {                              // if data added successfully
                        if(response.result==='Success'){
                            $( '#attend_form' ).each(function(){
                                this.reset();                                   // empty the form
                            });
                            alert(response.message)
                        }
                        else{
                            alert(response.message);                            // otherwise print unsuccessful message
                        }

                    }
                });
            });

            $('#course_id').on('click','.item',function (event) {      // if user clicks any item in course_id dropdown
                event.preventDefault();
                // alert($(this).data('course'));
                $(this).addClass('active');                            //  making that item active
            });

            $(document).ready(function() {
                $('#attend_table').DataTable();                 // for pagination
            } );


            $('#select_courses').on('click','.item',function (event) {    // if user clicks a course to view attendance

                event.preventDefault();
                var course_code=$(this).data('course');

                $('#attend_table tbody').find("tr:gt(0)").remove();       // cleaning old entries in table

                element = $('#attend_table tbody tr').last();
                $.ajax({
                    url: 'get_attendance',
                    type: 'GET',                                          // fetching attendance data of that course
                    data: {'course_id': course_code},
                    success: function (response) {                      // if data fetching was successful

                        var len=response.tuples.length;
                        for(var j=0;j<response.tuples.length;j++){
                            var name=response.stud_data.name[j];
                            var programme=response.stud_data.programme[j];
                            var batch=response.stud_data.batch[j];
                            var roll=response.tuples[j][1];
                            var course=course_code;
                            var present_attend=response.tuples[j][2];           // adding attendance data in table
                            var total_attend=response.tuples[j][3];
                            var attend_percent=((present_attend/total_attend)*100).toFixed(2);
                            txt="<tr>";
                            txt +='<td> '+(len-j)+ '</td>'+
                            '<td>' + name + '</td>' +
                            '<td>' + roll + '</td>' +
                            '<td>' + batch + '</td>' +
                            '<td>' + programme + '</td>' +
                            '<td>' + course + '</td>' +
                            '<td style="display:none;">' + total_attend + '</td>' +
                            '<td style="display:none;">' + present_attend + '</td>' +
                            '<td>' + attend_percent + '</td>'+
                            '<td> <a id="edit_tag"> <i  class="edit icon" style="font-size:1.3vw ; color:blue;"></i></a> &ensp; <a class="centered raised item" id="del_row"> <i id="bt" class="trash outline icon" style="font-size:1.3vw; color:red;"></i><br></a></td>';

                            txt +='</tr>';
                            element.after(txt);
                        }

                    },
                    error: function (response) {

                    }
                });
            });



        });