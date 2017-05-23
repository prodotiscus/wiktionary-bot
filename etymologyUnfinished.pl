use MediaWiki::Bot qw(:constants);
use utf8;
no warnings;

my $bot = MediaWiki::Bot->new({
    useragent   => 'MediaWiki::Bot 3.0.0 (User:...)',
    #assert      => 'bot',
    protocol    => 'https',
    host        => 'ru.wiktionary.org',
    path        => 'w',
    login_data  => { username => "...", password => "..." },
}) or die("BADLY!");
sub edit_unfinished_in_category
{
	my $category = @_[0];
	my @articles = $bot->get_pages_in_category("Category:$category",{ max => 0});
	foreach $article (@articles){
		if(not $article =~ m/^Категория:/g){
			my $text = $bot->get_text($article);
			$m = 'этимология:\|la';
			$r = 'unfinished|e=1';
			$e = 'e=1';
			if($text =~ m/$m/g and not $text =~ m/$e/g){
				$text =~ s/unfinished/$r/g;
			}
			print $text;
			$bot->edit({
				page    => $article,
				text    => $text,
				summary => 'Правка шаблона {{unfinished}}; добавление e=1; нужна'
			});
		}
	}
}
edit_unfinished_in_category("Латинский язык");
