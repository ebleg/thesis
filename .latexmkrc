$pdflatex = 'pdflatex -interaction=batchmode -halt-on-error  -shell-escape';
$pdf_mode = 1;
add_cus_dep( 'nlo', 'nls', 0, 'makenlo2nls' );
sub makenlo2nls {
system( "makeindex -s nomencl.ist -o \"$_[0].nls\" \"$_[0].nlo\"" );
}
