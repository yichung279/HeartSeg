$(document).ready(function() {  
  $("form button").click(function(event) {
    event.preventDefault();

    $.ajax({
      method: "get",
      url: "./img",
      data: {
        fname: $("form input[name='fname']").val(),
      },
      success: function(data) {
       $('#afterImg').remove()
       $('#beforeImg').remove()
       $('.board').append('<img id="beforeImg" src="' + data.before + '"></img>')
       $('.board').append('<img id="afterImg" src="' +data.after + '"></img>')
      
      }
    })
  

  })  
})
