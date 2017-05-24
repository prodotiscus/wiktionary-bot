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
}) or die("Cannot login!");
my @first_decl = ("veronica","Maria","magma","malaria","pina","concordia","idiota","pastinaca","lepra","Francia","blasphemia","apoplexia","apostata","chronologia","axilla","conjunctura","cosmopolita","melodia","miscellanea","primula","sappa","carpia","socolata","cerevisia","tulipa","Turcia","violina","tundra","Peruvia","Uraquaria","Uruguaia","chamomilla","infantia","neglegentia","hyaena","platea","wisteria","magnificentia","lipothymia","moneta","hyporeflexia","euphorbia","montuosa","tabuletta","Arctica","Baccha","Morchella","vodca","alauda","Bactria","naja","taenia","obba","agna","katana","tetrasticha","ichthyologia","chemica","alchemista","limma","sclera","hemicrania","samba","virologia","campana");
foreach $article (@first_decl){
    my $new_name = $article;
    $new_name =~ s/a$//g;
    my $text = $bot->get_text($article);
    $text =~ s/\{\{сущ la(\s|)\|/{{сущ la 1 i|$new_name|/g;
    $bot->edit({
    page    => $article,
    text    => $text,
    summary => 'автоматическая простановка первого склонения для латинских слов'
    });
    print "Edit of page $article\n";
}
