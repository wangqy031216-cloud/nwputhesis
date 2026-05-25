# latexmk configuration for nwputhesis
$pdf_mode = 5;  # 5 = xelatex mode

# Biber's packaged Perl cache can break in macOS's default TMPDIR.  Use a
# stable project-independent temp directory so bibliography compilation is
# reproducible when running plain `latexmk -xelatex bachelor.tex`.
my $biber_tmp = '/tmp/nwpu_biber_tmp';
mkdir $biber_tmp unless -d $biber_tmp;
$ENV{'TMPDIR'} = $biber_tmp;
$ENV{'TMP'} = $biber_tmp;
$ENV{'TEMP'} = $biber_tmp;

$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
