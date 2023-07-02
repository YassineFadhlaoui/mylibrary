import json
import os
import sys
from flask import Flask, jsonify, render_template, request, session

sys.path.append('..')
from mylibrary.helpers.helpers import load_config, init_logger, is_int, get_parameter
from mylibrary.controllers.books_controller import BooksController
from mylibrary.models.book import BookModel


app = Flask(__name__)
config_file = os.path.join("config", "mylibrary.conf")
config = load_config(config_file=config_file)
root_logger = init_logger(config=config)
books_controller = BooksController(config=config)
cover_folder = os.path.join("static", "covers")
app.secret_key = get_parameter("SECRET_KEYS", "SESSION_KEY", config)


@app.route("/status", methods=['GET'])
def show_status():
    """
    Return the status of the server
    """
    return jsonify({"status": "up"})


@app.route("/", methods=['GET'])
def show_home():
    """
    Show Home page with the list of all books and their related information
    """
    if not session.get('currently-reading'):
        session['currently-reading'] = len(books_controller.get_currently_reading())
    books = books_controller.get_all()
    return render_template('index.j2', books=books, currently_reading=session["currently-reading"], request_path=request.path)


@app.route("/add-to-library", methods=['GET'])
def add_book():
    """
    Show add book web page.
    """
    if not session.get('currently-reading'):
        session['currently-reading'] = len(books_controller.get_currently_reading())
    return render_template('add-book.j2', currently_reading=session["currently-reading"], request_path=request.path)


@app.route("/currently-reading", methods=['GET'])
def get_currently_reading():
    """
    Show the books that are not yet finished
    """
    try:
        currently_reading = books_controller.get_currently_reading()
        session["currently-reading"] = len(currently_reading)
        return render_template('index.j2', books=currently_reading, currently_reading=len(currently_reading), request_path=request.path), 200

    except Exception:
        root_logger.exception("An exception occurred while processing request")
        return jsonify({
            "success": False,
            "error": "Failed to process your request"
        }), 500


@app.route("/add_book/", methods=['POST', 'PUT'])
def add():
    """
    Add book endpoint: add books to the library database.
    The UI will send a data form to that endpoint, we parse the text data and the multipart data. Then we build a BookModel instance
    based on that data, and we persist it to the database.
    """
    try:
        # We read the book text data
        new_book_text_data = request.form
        # read the title
        book_title = new_book_text_data.get("title")
        # read the author
        book_author = new_book_text_data.get("author")
        # read book notes
        book_notes = new_book_text_data.get("notes")
        # read progress
        book_progress = new_book_text_data.get("progress")
        # make sure that all required fields are set
        for book_info in [book_title, book_author, book_progress]:
            if not book_info:
                # return a bad request due missing field(s)
                return jsonify({
                    "success": False,
                    "error": "book title, book author and the progress field should not be left blank"
                }), 400
        # return a bad request when the submitted progress is not within the range [0,100]
        if not is_int(book_progress) or int(book_progress) < 0 or int(book_progress) > 100:
            return jsonify({
                "success": False,
                "error": "progress should be an integer in the interval [0,100]"
            }), 400
        # Get the book cover
        new_book_cover_data = request.files
        book_cover = new_book_cover_data.getlist('file')
        book_cover_path = None
        if book_cover and book_cover[0].mimetype in ['image/jpeg', 'image/png']:
            # set the file name to the book title
            book_cover_name = f"{book_title.lower().replace(' ', '_')}.{book_cover[0].mimetype.split('/')[1]}"
            # set the cover path
            book_cover_path = os.path.join(cover_folder, book_cover_name)
            # save the file to the specified path
            book_cover[0].save(book_cover_path)
        # build a BookModel from the extracted information
        new_book = BookModel(
            title=book_title.lower(),
            author=book_author,
            cover=book_cover_path,
            finished=True if int(book_progress) == 100 else False,
            progress=int(book_progress),
            notes=book_notes
        )
        # try to add the book
        is_added, error = books_controller.add(new_book)

        if is_added:
            # try to make the currently reading books span
            if not int(book_progress) == 100:
                session['currently-reading'] = session['currently-reading'] + 1
            root_logger.info("book is added successfully to the library")
            return jsonify({
                "success": True,
                "error": f"book {book_title} is successfully added to your library"
            }), 200
        elif error == "Book already exists":
            root_logger.error("book already exists in the library")
            return jsonify({
                "success": False,
                "error": f"book {book_title} already exists"
            }), 409
        else:
            root_logger.error("Failed to add book due to an internal server")
            return jsonify({
                "success": False,
                "error": f"failed to add book {book_title}"
            }), 500
    except Exception:
        root_logger.exception("failed to add book")
        return jsonify({
            "success": False,
            "error": "failed to add book due to an internal error"
        })


@app.route("/update/", methods=['POST', 'PUT'])
def update():
    """
    Update book endpoint: This endpoint is intended to be contacted by the UI to update the progress or/and the book notes
    """
    try:
        # load the update data as json
        update_data = json.loads(request.data.decode("utf-8"))
    except Exception:
        return jsonify({
            "success": False,
            "error": "Failed to parse request body"
        }), 400

    try:
        book_title = update_data["title"]
        if not is_int(update_data.get("progress")) or int(update_data.get("progress")) > 100 or int(update_data.get("progress")) < 0:
            root_logger.info("Skipping progress")
            progress = None
        else:
            progress = int(update_data.get("progress"))
        root_logger.info("update")
        books_controller.update(
            BookModel(
                title=book_title,
                author="",
                cover="",
                finished=False,
                progress=progress,
                notes=update_data.get("notes")
            )
        )
        if not int(update_data.get("progress")) == 100:
            session['currently-reading'] = session['currently-reading'] + 1
    except Exception:
        root_logger.exception("An exception occurred while processing request")
        return jsonify({
            "success": False,
            "error": "Failed to update the requested book information due to an internal error"
        }), 500

    return jsonify({
        "success": True
    }), 200


@app.route("/delete/", methods=['POST', 'PUT'])
def delete():
    """
    Delete book endpoint: this endpoint is contacted by the UI when the User is trying to delete a book
    """
    root_logger.info("deleting book")
    try:
        delete_data = json.loads(request.data.decode("utf-8"))
    except Exception:
        return jsonify({
            "success": False,
            "error": "Failed to parse request body"
        }), 400

    try:
        book_title = delete_data["title"]
        result = books_controller.delete(book_title)
        if result:
            return jsonify({
                "success": True
            }), 200
        raise Exception("Book to delete does not exist")
    except Exception:
        root_logger.exception("An exception occurred while processing request")
        return jsonify({
            "success": False,
            "error": "Failed to delete book"
        }), 500
