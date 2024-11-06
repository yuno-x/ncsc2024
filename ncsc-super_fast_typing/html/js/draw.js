var ctx, image;

window.onload = () =>
{
    const canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");

    post_word( ":start:" );
};

function draw( imgb64 )
{
    image = new Image();
    image.src = "data:image/png;base64," + imgb64;
    image.onload = () => {
        ctx.save();
        canvas.width = image.naturalWidth;
        canvas.height = image.naturalHeight;
        ctx.drawImage( image, 0, 0 );
        ctx.restore();
    };
}

function post_word( word )
{
    $.ajax(
        { type: "POST", url: "typing.php", dataType: 'json', data: { "word": word } }
    ).done(
        function( res )
        {
            document.getElementById( 'msg' ).innerText = res.msg;
            if( res.imgb64 != "" )
            {
                draw( res.imgb64 );
            }
        }
    ).fail(
        function( XMLHttpRequest, textStatus, error )
        {
            alert( error );
        }
    ).always(
        function()
        {
            document.form.word.value = "";
        }
    );
}

function send_word()
{
    var word = document.form.word.value;
    if( word != "" )
    {
        post_word( word );
    }
}
