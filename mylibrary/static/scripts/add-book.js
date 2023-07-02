const choose_file = document.getElementById("new_book_cover");
const cover_preview = document.getElementById("cover_preview");

choose_file.addEventListener("change", function () {
  get_img_data();
});


function get_img_data() {
  const files = choose_file.files[0];
  if (files) {
    const file_reader = new FileReader();
    file_reader.readAsDataURL(files);
    file_reader.addEventListener("load", function () {
      cover_preview.style.display = "block";
      cover_preview.innerHTML = '<img class="align-middle" src="' + this.result + '" />';
    });
  }
}


$(document).ready(function () {
    $("form#new_book_form").submit(function(event) {
        //stop submit the form, we will post it manually.
        event.preventDefault();
        var book_form = new FormData();
        // add the title
        book_title=$('#new_book_title').val()
        book_form.append('title', book_title)
        // add the author
        book_author=$('#new_book_author').val()
        book_form.append('author', book_author)
        // add the progress
        book_progress=$('#new_book_progress').val()
        book_form.append('progress', book_progress)
        // add the book notes
        book_notes=$('#new_book_notes').val()
        book_form.append('notes', book_notes)
        // add the cover
        book_cover=$('#new_book_cover')[0]
        if(book_cover.files && book_cover.files.length >= 1){
                book_form.append("file", book_cover.files[0] , book_cover.files[0].name);
        }

        // disabled the submit button
        $("#submit_book").prop("disabled", true);

        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "/add_book",
            data: book_form,
            processData: false,
            contentType: false,
            timeout: 3000,
            cache: false,
            success: function (data) {
                console.log("SUCCESS : ", data);
                alert("book "+ book_title +" is added successfully to the library")
                $("#submit_book").prop("disabled", false);
            },
            error: function (e) {
                $("#submit_book").prop("disabled", false);
                console.log("ERROR : ", e);
                alert("failed to add book "+book_title+" to the library due to the error: "+ e.responseJSON.error)

            }
        });
    });
});