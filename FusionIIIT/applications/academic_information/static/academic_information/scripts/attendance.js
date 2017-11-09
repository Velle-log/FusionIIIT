$(document).ready(function () {

            $(document).on('submit','#cse_attend_form',function (event) {
                event.preventDefault();

                $.ajax({
                    url: 'attendance',
                    type: 'POST',
                    data: {
                        student_id: $('#student_id').val(),
                        course_id: $('#course_id').val(),
                        present_attend: $('#present_attend').val(),
                        total_attend: $('#total_attend').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (response) {
                        if(response.result==='Success'){
                            $( '#cse_attend_form' ).each(function(){
                                this.reset();
                            });
                        }
                        else{
                            alert(response.message);
                        }

                    }
                });
            });

            $(document).on('submit','#ece_attend_form',function (event) {
                event.preventDefault();

                $.ajax({
                    url: 'attendance',
                    type: 'POST',
                    data: {
                        student_id: $('#student_id_ece').val(),
                        course_id: $('#course_id_ece').val(),
                        present_attend: $('#present_attend_ece').val(),
                        total_attend: $('#total_attend_ece').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (response) {
                        if(response.result==='Success'){
                            $( '#ece_attend_form' ).each(function(){
                                this.reset();
                            });
                        }
                        else{
                            alert(response.message);
                        }

                    }
                });
            });

            $(document).on('submit','#mech_attend_form',function (event) {
                event.preventDefault();

                $.ajax({
                    url: 'attendance',
                    type: 'POST',
                    data: {
                        student_id: $('#student_id_mech').val(),
                        course_id: $('#course_id_mech').val(),
                        present_attend: $('#present_attend_mech').val(),
                        total_attend: $('#total_attend_mech').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (response) {
                        if(response.result==='Success'){
                            $( '#mech_attend_form' ).each(function(){
                                this.reset();
                            });
                        }
                        else{
                            alert(response.message);
                        }

                    }
                });
            });


            $(document).on('submit','#design_attend_form',function (event) {
                event.preventDefault();

                $.ajax({
                    url: 'attendance',
                    type: 'POST',
                    data: {
                        student_id: $('#student_id_design').val(),
                        course_id: $('#course_id_design').val(),
                        present_attend: $('#present_attend_design').val(),
                        total_attend: $('#total_attend_design').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (response) {
                        if(response.result==='Success'){
                            $( '#design_attend_form' ).each(function(){
                                this.reset();
                            });
                        }
                        else{
                            alert(response.message);
                        }

                    }
                });
            });

            
            $('#cse_courses').on('click','button',function (event) {

                event.preventDefault();
                var course_code=$(this).data('course');
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

            $('#ece_courses').on('click','button',function (event) {

                event.preventDefault();
                var course_code=$(this).data('course');
                $('#ece_table tbody').find("tr:gt(0)").remove();

                element = $('#ece_table tbody tr').last();
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

            $('#mech_courses').on('click','button',function (event) {

                event.preventDefault();
                var course_code=$(this).data('course');
                $('#mech_table tbody').find("tr:gt(0)").remove();

                element = $('#mech_table tbody tr').last();
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

            $('#design_courses').on('click','button',function (event) {

                event.preventDefault();
                var course_code=$(this).data('course');
                $('#design_table tbody').find("tr:gt(0)").remove();

                element = $('#design_table tbody tr').last();
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