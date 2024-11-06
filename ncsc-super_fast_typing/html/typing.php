<?php
session_start();

function appreciate()
{
    $duration = time() - $_SESSION["start"];
    session_unset();
    if( $duration < 3 )
    {
        return "God\nflag{you_should_use_ocr}";
    }
    else if( $duration < 8 )
    {
        return  "Wizzard";
    }
    else if( $duration < 10 )
    {
        return "Super Star";
    }
    else if( $duration < 12 )
    {
        return "Professional";
    }
    else if( $duration < 14 )
    {
        return "S+";
    }
    else if( $duration < 16 )
    {
        return "S-";
    }
    else if( $duration < 18 )
    {
        return "A+";
    }
    else if( $duration < 20 )
    {
        return "A-";
    }
    else if( $duration < 22 )
    {
        return "B+";
    }
    else if( $duration < 24 )
    {
        return "B-";
    }
    else if( $duration < 26 )
    {
        return "C+";
    }
    else if( $duration < 28 )
    {
        return "C-";
    }
    else if( $duration < 30 )
    {
        return "D+";
    }
    else if( $duration < 32 )
    {
        return "D-";
    }
    else if( $duration < 34 )
    {
        return "E+";
    }
    else if( $duration < 36 )
    {
        return "E-";
    }
    else
    {
        return "F";
    }
}

function main()
{
    $input = $_POST["word"];

    if( $input === ":start:" )
    {
        $_SESSION["start"] = time();
        $_SESSION["count"] = 10;
        $msg = "";
    }
    else
    {
        if( !isset( $_SESSION["count"] ) || $_SESSION["count"] == 0 )
        {
            $res = [ "imgb64" => "", "msg" => "Restart to input `:start:`." ];
            echo json_encode( $res );
            exit();
        }

        $msg = "incorrect!";
        if( $input === $_SESSION["word"] )
        {
            $msg = "correct!";
            $_SESSION["count"]--;
            if( $_SESSION["count"] == 0 )
            {
                $imgb64 = "";
                $msg .= "\nScore: " . appreciate();

                $res = [ "imgb64" => $imgb64, "msg" => $msg ];
                echo json_encode( $res );
                exit();
            }
        }
    }

    $wordlist = file( "../wordimg/wordlist.txt", FILE_IGNORE_NEW_LINES );
    $list_size = count( $wordlist );
    $idx = rand( 0, $list_size - 1 );
    $word = $wordlist[$idx];
    $filename = "../wordimg/" . $word . ".png";
    if( file_exists( $filename ) )
    {
        $imgdata = file_get_contents( $filename );
        $imgb64 = base64_encode( $imgdata );
    }
    $res = [ "imgb64" => $imgb64, "msg" => $msg ];
    $_SESSION["word"] = $word;

    echo json_encode( $res );
}

main();
?>
