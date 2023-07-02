


function delete_book(book_title) {
    $.ajax({
      type: "POST",
      url: "/delete",
      data: JSON.stringify(
        {
        "title": book_title
      }),
      success: function(data, status){
        $("#"+book_title.toLowerCase().replace(' ','_')+"_delete_modal").modal('hide')
        alert("Delete operation for book '"+book_title+"' succeeded")
        location.reload(true)
      },
      error: function(data, status){
        $("#"+book_title.toLowerCase().replace(' ','_')+"_delete_modal").modal('hide')
        alert("Delete operation for book '"+book_title+"' failed")
      },
      dataType: "json",
      contentType : "application/json"
    });
}

function update_book(book_title) {
    var progress = $("#"+book_title.toLowerCase().replace(' ','_')+"_update_modal_progress").val();
    var notes=$("#"+book_title.toLowerCase().replace(' ','_')+"_update_modal_notes").val();
    $.ajax({
      type: "POST",
      url: "/update",
      data: JSON.stringify(
        {
        "title": book_title,
        "progress": progress,
        "notes": notes
      }),
      success: function(data, status){
        $("#"+book_title.toLowerCase().replace(' ','_')+"_update_modal").modal('hide')
        alert("Update operation for book '"+book_title+"' succeeded")
        location.reload(true)
      },
      error: function(data, status){
        $("#"+book_title.toLowerCase().replace(' ','_')+"_update_modal").modal('hide')
        alert("Update operation for book '"+book_title+"' failed")
      },
      dataType: "json",
      contentType : "application/json"
    });
}







