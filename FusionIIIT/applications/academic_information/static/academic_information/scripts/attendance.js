$(document).ready(function () {

            $(document).on('submit','#attend_form',function (event) {
                event.preventDefault();
                var element=$('#course_id .active');
                var course_code=element.data('course');
                $.ajax({
                    url: 'attendance',
                    type: 'POST',
                    data: {
                        student_id: $('#student_id').val(),
                        course_id: course_code,
                        present_attend: $('#present_attend').val(),
                        total_attend: $('#total_attend').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (response) {
                        if(response.result==='Success'){
                            $( '#attend_form' ).each(function(){
                                this.reset();
                            });
                        }
                        else{
                            alert(response.message);
                            alert(element);
                        }

                    }
                });
            });

            $('#course_id').on('click','.item',function (event) {
                event.preventDefault();
                // alert($(this).data('course'));
                $(this).addClass('active');
            });

            
            $('#cse_courses').on('click','.item',function (event) {

                event.preventDefault();
                var course_code=$(this).data('course');
                alert(course_code);
                $('#cse_table tbody').find("tr:gt(0)").remove();

                element = $('#cse_table tbody tr').last();
                $.ajax({
                    url: 'get_attendance',
                    type: 'GET',
                    data: {'course_id': course_code},
                    success: function (response) {


                        for(var j=0;j<response.tuples.length;j++){
                            var name=response.stud_data.name[j];
                            var programme=response.stud_data.programme[j];
                            var batch=response.stud_data.batch[j];
                            var roll=response.tuples[j][1];
                            var course=course_code;
                            var present_attend=response.tuples[j][2];
                            var total_attend=response.tuples[j][3];
                            var attend_percent=((present_attend/total_attend)*100).toFixed(2);
                            txt="<tr>";
                            txt +='<td>  </td>'+
                            '<td>' + name + '</td>' +
                            '<td>' + roll + '</td>' +
                            '<td>' + batch + '</td>' +
                            '<td>' + programme + '</td>' +
                            '<td>' + course + '</td>' +
                            '<td>' + attend_percent + '</td>'+
                            '<td>  <i class="refresh icon" style="font-size:1.3vw"></i>' +
                            '<button type="submit" id="'+roll+'"> <i class="trash outline icon" style="font-size:1.3vw"></i> </button></td>' ;

                            txt +='</tr>';
                            element.after(txt);
                        }

                        console.log(response.stud_data.name.length);
                        console.log(response.tuples.length);




   
                    },
                    error: function (response) {

                    }
                });
            });



        });