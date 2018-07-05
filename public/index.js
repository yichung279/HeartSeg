$(document).ready(function() {  
  $("#form button").click(function(event) {
    event.preventDefault();
    
    $('#afterImg').remove()
    $('#beforeImg').remove()
    $('#nofile').remove()
    $('.board').append('<p id="loading">loading</p>')
    
    $.ajax({
      method: "get",
      url: "./img",
      data: {
        fname: $("#form input[name='fname']").val(),
      },
      success: function(data) {
        if(data.img_exist){
          $('#loading').remove()
          $('.board').append('<img id="beforeImg" src="data/' + data.before + '"></img>')
          $('.board').append('<img id="afterImg" src="result/' +data.after + '"></img>')
        }else{
          $('#loading').remove()
          $('.board').append('<p id="nofile">無此檔案</p>')
        }
      }
    })
  

  })  
})
