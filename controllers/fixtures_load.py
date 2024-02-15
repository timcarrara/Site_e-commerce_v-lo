#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS adresse, ligne_panier, ligne_commande,
                     commande, etat, taille, utilisateur, type_velo, velo;'''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE taille (
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(255),
    PRIMARY KEY(id_taille)
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE type_velo (
    id_type_velo INT AUTO_INCREMENT,
    libelle_type_velo VARCHAR(255),
    PRIMARY KEY(id_type_velo)
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    nom VARCHAR(255),
    PRIMARY KEY (id_utilisateur)
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE velo (
    id_velo INT AUTO_INCREMENT,
    nom_velo VARCHAR(255),
    prix_velo DECIMAL(10, 2),
    taille_id INT NOT NULL,
    type_velo_id INT NOT NULL,
    matiere VARCHAR(255),
    description VARCHAR(4500),
    fournisseur VARCHAR(255),
    marque VARCHAR(255),
    image VARCHAR(255),
    stock INT,
    PRIMARY KEY(id_velo),
    FOREIGN KEY (taille_id) REFERENCES taille(id_taille) ON DELETE CASCADE,
    FOREIGN KEY (type_velo_id) REFERENCES type_velo(id_type_velo) ON DELETE CASCADE
    ) DEFAULT CHARSET utf8;'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE etat (
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),
    PRIMARY KEY (id_etat)
    ) DEFAULT CHARSET=utf8'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATETIME,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_commande (
    commande_id INT,
    velo_id INT,
    prix NUMERIC(10,2),
    quantite_commande INT,
    PRIMARY KEY (commande_id, velo_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande) ON DELETE CASCADE,
    FOREIGN KEY (velo_id) REFERENCES velo(id_velo)
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_panier (
    utilisateur_id INT,
    velo_id INT,
    date_ajout DATETIME,
    quantite_panier INT,
    PRIMARY KEY (utilisateur_id, velo_id, date_ajout),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (velo_id) REFERENCES velo(id_velo)
    ) DEFAULT CHARSET=utf8;'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE adresse (
    id_adresse INT AUTO_INCREMENT,
    utilisateur_id INT,
    nom_client VARCHAR(255),
    rue VARCHAR(255),
    code_postal INT,
    ville VARCHAR(255),
    valide INT,
    PRIMARY KEY (id_adresse),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)


    sql = '''INSERT INTO taille (libelle_taille) VALUES
('XS'),
('S'),
('M'),
('L'),
('XL');
    '''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO type_velo (libelle_type_velo) VALUES
('Vélo gravel'),
('VTT'),
('Vélo électrique'),
('Vélo de ville'),
('Vélo de trekking'),
('Vélo enfant & ado'),
('BMX'),
('VTC'),
('Vélo de route');

    '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO velo (nom_velo, prix_velo, taille_id, type_velo_id, matiere, description, fournisseur, marque, image, stock) VALUES
('Kona Rove SE', 1599.00, 1, 1, 'Acier', 'Le Rove est devenu le vélo de prédilection pour des personnes du monde entier qui ont simplement envie de... partir ! Il est spécifié de manière optimale, agréable à regarder, le Rove facilite les déplacements quotidiens, les sentiers en gravier, ou la sortie sportive après le travail sur la colline locale. Le Rove est le vélo CrMo 650x47c insaisissable que vous pouvez vous permettre. Il était branché avant que la tendance ne devienne branchée. C''est un vélo qui veut rouler partout où VOUS voulez rouler. Tube de direction conique : Un diamètre plus important à la base du tube de direction distribue mieux la force de choc, prolongeant la durée de vie du roulement du jeu de direction lui-même et éliminant les vibrations des freins, tout en offrant une performance de direction confiante. La force inhérente de sa conception triangulaire signifie également une position de direction plus solide et un équilibre amélioré, offrant au cycliste plus de contrôle sur un terrain accidenté. Un tube de direction conique, de type "zero-stack", place également la force là où elle va - dans la partie inférieure du jeu de direction - maximisant la durabilité du roulement là où c''est nécessaire. Roues de 650b : Les roues et pneus de 650b ont un diamètre global similaire à celui d''un pneu traditionnel de 700c pour gravier ou de déplacement, mais avec une jante de diamètre inférieur et un pneu plus large et plus haut. Le volume d''air supplémentaire dans cette nouvelle génération de pneus urbains et mixtes signifie qu''ils peuvent être utilisés confortablement à des pressions plus basses tout en roulant rapidement sur une variété de surfaces. C''est le meilleur des deux mondes.', 'Kona', 'Kona', 'kona-rove-se.jpg', 0),
('Vitus Mythique 29 VRS', 2099.99, 2, 2, 'Aluminium', 'La nouvelle génération du Mythique s''appuie sur son héritage primé et est un vélo de trail en aluminium axé sur la performance. C''est un vélo polyvalent idéal, dont chaque modèle est équipé de composants soigneusement sélectionnés, parfaitement adaptés les uns aux autres, pour un maximum de plaisir sur les sentiers. Nous avons tous notre trail préféré. Ce n''est peut-être pas le plus technique, il n''a peut-être pas les virages les plus raides ou les descentes qui donnent des sueurs froides, mais ce flow est tellement agréable à conduire. On peut en imaginer chaque centimètre. Chaque montée, chaque descente et chaque virage. Élu. Le Vitus Mythique 29 VRS procure exactement cette sensation de légèreté et renforce votre confiance grâce à sa capacité et à son contrôle éprouvés, de sorte que chaque sentier vous donne l''impression d''être un nouveau favori. Le Mythique ne se soucie pas de votre style de conduite ou de l''endroit où vous roulez - il apporte simplement le plaisir. L''inconvénient ? Combien de temps vous devez attendre que vos copains vous rejoignent. Le but du Mythique n''est pas nécessairement de devenir aussi grossier et frénétique que possible, mais si tu cherches à faire quelque chose de plus agressif, il suivra volontiers. C''est un vélo de trail qui est maniable et ludique sans être incontrôlable. Rétrécissez-le avec légèreté ou relâchez-vous et libérez tout votre potentiel de trail. C''est une performance constante tout au long du parcours de la part d''un vélo qui gère les sections techniques avec calme, équilibre et sérénité. La conception de la suspension est une plateforme qui a fait ses preuves depuis longtemps et qui permet de mieux prévenir les coups de pédale lors de l''escalade et de rester prévisible lors du freinage. Grâce aux composants fiables Shimano Deore, dont une transmission à vitesses, ce vélo est immédiatement prêt à rouler. La Mythique est une bête de somme à ne pas sous-estimer - digne de confiance et contrôlée - avec une capacité à dompter les sentiers qui est bien au-dessus de son niveau de prix. C''est un vélo qui inspire confiance, sans définir ton style - le flair vient de toi, le vélo t''aide juste à suivre la ligne parfaite. Géométrie mise à jour : Côte à côte, les changements sont clairement visibles. À l''avant, le tube de direction est plus plat de 0,5 (66 contre 65,5 avec une fourche de 140 mm), ce qui permet un meilleur contrôle sur un plus large éventail de terrains, en particulier lorsqu''ils deviennent plus raides et plus techniques. Ceci est compensé par un angle de tube de selle effectif révisé, plus raide de 1,5 (76 à 77,5 avec une fourche de 140 mm), qui reflète le reach modifié et positionne le cycliste plus au-dessus du boîtier de pédalier pour une escalade plus efficace. Reach : Vitus ne réserve pas les fonctionnalités aux modèles haut de gamme. Surtout lorsqu''il s''agit de la géométrie - si elle profite à tous les cyclistes, elle est utile dans tous les segments de prix. Vitus a regardé de plus près le Sommet et l''Escarpe et a adapté la géométrie en conséquence, de sorte que le Mythique est beaucoup plus réactif dans les montées. Vous ne vous sentirez plus flasque et inerte à l''arrière du vélo. Slam the Dropper. Le nouveau Mythique peut désormais être équipé d''un dropper complet dans toutes les tailles, ce qui vous permet de maximiser votre liberté de mouvement et de récupérer du poids lorsque le trail descend. Maintenu simple : Rien ne gâche autant le plaisir de rouler que les normes et le jargon de l''industrie du. Le Mythique veut rester simple. L''accent est mis sur des travaux de maintenance et d''entretien aussi simples que possible pour le client. L''utilisation de pièces, de roulements et de matériel qui ont une longue durée de vie et sont largement disponibles. Des pièces qui ont été minutieusement testées sur le Mythique dans toutes les conditions.', 'Vitus', 'Vitus', 'haibike-trekking-4-trapeze.jpg', 1),
('HAIBIKE Trekking 4 Trapèze', 3099.00, 2, 3, 'Aluminium', 'Avec le nouveau Trekking 4 Lowstandover, tu es parfaitement équipé pour les longues randonnées grâce à sa géométrie extra-confortable. Le puissant moteur Yamaha PW-TE te donne à tout moment la puissance nécessaire pour parcourir de nombreux kilomètres, que ce soit sur le chemin du travail ou lors d''une randonnée de plusieurs jours avec des bagages. L''équipement conforme au StVZO fait de cet eTrekkingbike le compagnon idéal pour toutes tes excursions. ', 'HAIBIKE', 'HAIBIKE', 'haibike-trekking-4-trapeze.jpg', 2),
('Cinelli Zydeco', 1299.00, 3, 1, 'Aluminium', 'Cinelli s''affirme comme la référence du gravel avec son légendaire modèle Zydeco, qui s''est développé au fil des années à partir de la discipline du cyclocross. Aujourd''hui, les performances améliorées du frein à disque mécanique à axe traversant sont associées au choix du groupe MicroSHIFT R9. Grâce à la courbe accentuée, la prise en main du levier ergonomique est plus sûre, pour un contrôle total sur tous les terrains. Une autre nouveauté est la selle San Marco Era avec des graphismes customisés Zydeco. ', 'Cinelli', 'Cinelli', 'cinelli-zydeco.jpg', 0),
('3T Exploro Race Ekar 1X13', 5799.00, 4, 1, 'Carbone', '3T Exploro Race Ekar - L''aéro sur la terre avec l''élégance italienne. Une ambiance de course à l''italienne pour l''asphalte, la terre et tout ce qui se trouve entre les deux : Le 3T Exploro Race avec le Campagnolo Ekar n''est pas seulement très élégant, il est aussi très performant. Avec elle, tu es rapide aussi bien sur les chemins que sur la route - et en plus, tu es rapide lorsque le terrain devient encore plus accidenté. Le 3T Exploro a été le premier gravelbike au monde à être optimisé en termes d''aérodynamisme. Le cadre Racemax sur lequel est basé ce modèle fait évoluer le concept initial sur plusieurs points, le rendant encore plus rapide et confortable. Non seulement tu as le potentiel pour être en tête des courses de gravel, mais tu peux aussi remplacer tous tes vélos à guidon de course. Vélo de course ou gravel bike ? Les deux ! Avec presque tous les vélos de gravel, tu es confronté au choix difficile d''échanger la vitesse d''un vélo de course contre le confort et l''aptitude au tout-terrain. L''Exploro ne fait pas de compromis, ce que tu peux déjà constater par sa position de conduite agressive. Tu seras vraiment au courant la première fois que tu prendras la route : Le cadre rigide se propulse vers l''avant et une fois que tu as pris de la vitesse, les nombreuses caractéristiques aéro, comme le tube diagonal massif qui absorbe le flux d''air des pneus larges et le dirige autour des bidons, ou la découpe dans le tube de selle, se révèlent payantes. 650b ou 700c : Combien de pneus peut-on utiliser ? Selon le terrain que tu préfères, tu as besoin de différentes quantités de gomme et l''Exploro a de la place pour (presque) tout le monde. Si vous voulez aller très vite sur du gravel modéré, des pneus de 46 millimètres de large sur des roues de 700c-Laufr conviennent. Cela te permet de rouler en tête de chaque groupe de tête. Si tu souhaites rouler plus tranquillement ou si un terrain plus exigeant t''attend, tu opteras pour des roues plus petites de 650b-Laufr avec des pneus de d''une largeur maximale de 61 millimètres. D''ailleurs, on ne joue plus aux devinettes pour savoir si ton pneu est adapté. Avec le Racemax, 3T a introduit le concept de WAM (Width As Measured) et indique ainsi toute la liberté des pneus. Oublie donc la largeur de pneu imprimée, parfois imprécise, et mesure simplement la largeur réelle de ton pneu sur les roues que tu utilises. Rapide, pas seulement en soufflerie : L''Exploro est rapide dans la vie réelle et pas seulement dans un montage expérimental théorique en soufflerie. Cela commence par le fait que les performances aérodynamiques du cadre ont été testées avec les profils "Sqaero" à une vitesse réaliste de 20 miles par heure. La norme est de 30 miles à l''heure, ce qui souligne les avantages aérodynamiques tout en créant des attentes excessives. De plus, tous les tests ont été effectués avec des bidons sur le vélo, car les longues randonnées ne sont pas possibles sans eau. Ainsi, un Exploro sale avec des pneus larges et des bidons est plus rapide qu''un vélo de course sans caractéristiques aéro avec des pneus de 28 millimètres de large et sans bidon. Il est optimisé pour des largeurs de pneus comprises entre 35 et 46 millimètres et, dans ce domaine, il tient tête aux vélos de course rapides sur le plan purement aérodynamique. Campagnolo Ekar : Il n''y a probablement pas de meilleur groupe de vitesses pour un 3T Exploro qu''un Campagnolo Ekar. Tant le cadre que le groupe incarnent la volonté d''innover, de dépasser les limites et une bonne dose de style. Le seul dérailleur vitesses spécifique à la gravelle à l''heure actuelle s''adapte parfaitement, ne serait-ce que par son concept, à ce vélo de gravel aéro révolutionnaire. Bien sûr, il n''y a pas de mal à ce que les 13 vitesses, avec le petit pignon de, fournissent un énorme éventail de vitesses qui te permettront de gravir toutes les côtes. En descendant, tu peux recourir à des freins considérés comme les meilleurs freins hydrauliques pour vélos de route sur le marché.', '3T', '3T', '3t-exploro-race-ekar-1x13.jpg', 10),
('Ortler Van Dyck Trapèze', 499.00, 3, 4, 'Acier', 'Découvre ce classique riche en traditions, doté d''un équipement moderne et fiable. La nostalgie à l''état pur - un beau design intemporel et un artisanat solide donnent naissance à un vélo hollandais on ne peut plus classique. Fabriqué selon la méthode traditionnelle du manchon en acier résistant et doté d''une vision de l''essentiel. Réduit, mais extrêmement fonctionnel et durable - un vrai vélo Ortler de qualité. L''Ortler Van Dyck s''adresse à tous ceux qui recherchent un vélo moderne dans le style du bon vieux "vélo hollandais". Le mot d''ordre était clair : Simplicité et réduction à l''essentiel pour réaliser un vélo hollandais avec une finition de haute qualité à un prix attractif. La peinture en poudre résistante aux chocs scelle de manière fiable le cadre en acier à la finition soignée. L''absence de composants sensibles à l''usure et la vitesse au moyeu Shimano Nexus à vitesses avec frein à rétropédalage font de l''Ortler Van Dyck un compagnon fidèle pour des années. Le tout est complété par une dynamo de moyeu Shimano fiable et un feu de position arrière moderne à LED. L''Ortler Van Dyck devient ainsi le compagnon idéal dans la vie quotidienne en ville. Grâce à l''enjambement bas et à la grande plage de réglage du guidon et de la selle, les cyclistes mesurant entre 1,55 m et 1,85 m peuvent rouler confortablement avec le cadre Ortler Van Dyck Unisize.', 'Ortler', 'Ortler', 'ortler-van-dyck-trapeze.jpg', 10),
('Winora Domingo 27 Sport Trapèze', 1049.00, 4, 5, 'Aluminium', 'Le WINORA Domingo 27 Sport est toujours prêt pour les randonnées du week-end, les trajets quotidiens et les courses rapides. Grâce à la géométrie sportive et à la fourche suspendue SR Suntour, tu es également bien équipé pour les sorties en terrain facile. La transmission Alivio à vitesses de Shimano, parfaitement démultipliée, te permet de surmonter les montées les plus raides et les freins à disque hydrauliques bien dosés te ramènent à l''arrêt en toute fiabilité en descente et par tous les temps. Ce vélo de trekking stylé est disponible en modèle femme et homme. ', 'Winora', 'Winora', 'winora-domingo-27-sport-trapeze.jpg', 10),
('Scool niXe alloy 18 Enfant', 289.00, 1, 6, 'Aluminium', 'Des vélos pour enfants qui font immédiatement battre le cœur des enfants. Multicolore, plein de vie et surtout cool ! Pour les parents, les vélos peuvent marquer des points grâce à leur qualité et à leurs détails adaptés aux enfants. Le cadre en aluminium robuste et nécessitant peu d''entretien, 1-Gang le moyeu de la roue arrière à vitesse, les puissants freins V-Brake et un frein à rétropédalage fiable sont autant d''éléments convaincants. ', 'Scool', 'Scool', 'scool-nixe-alloy-18-kids.jpg', 10),
('Serious Bear Rock LTD', 2499.00, 1, 3, 'Aluminium', 'Serious Bear Rock LTD - Votre départ dans le monde du VTT électrique. Le Serious Bear Rock vous garantit un départ puissant dans le monde des vélos tout terrain électriques. Ce semi-rigide en aluminium, sportif et stable, équipé d''un moteur Bosch Performance, offre 75 newton mètres de puissance dans les montées ainsi qu''une bonne dynamique de conduite et impressionne par son caractère authentique de vélo tout terrain sur les sentiers. La combinaison de grandes roues stables de 29" pouces avec des jantes à double paroi et une fourche avec un débattement de suspension de 100 millimètres lui permet de rouler en toute confiance sur les obstacles des sentiers et d''offrir des caractéristiques de conduite agiles. Les pneus Schwalbe de 2.25" pouces offrent une grande traction, des caractéristiques très satisfaisantes de roulement ainsi qu''une protection contre les crevaisons. Si vous le souhaitez, vous pouvez également monter des pneus tubeless. Les freins à disque entièrement hydrauliques permettent de bien contrôler le vélo à chaque sortie. Les dix vitesses combinées au moteur Bosch suffisent à franchir les pentes les plus raides. La batterie standard de Wh apporte un supplément de soutien et d''autonomie. Le VTT électrique Serious Bear Rock est idéal pour les randonnées plus rapides et plus longues. Il est aussi parfait lorsque vous voulez vous détendre !', 'Serious', 'Serious', 'serious-bear-rock.jpg', 10),
('Kona Honzo', 1599.00, 1, 2, 'Aluminium', 'Le Honzo était le premier hardtail aux courbes profondes, adapté au trail. Sa géométrie progressive a certes été revue au fil des ans, mais son attitude enjouée n''a pas changé d''un iota. C''est le qui ne se sent pas comme un, l''ami fiable qui est toujours prêt à faire la fête et qui t''accompagne dans toutes les situations. 12 x 148 mm axe de roue arrière Les standards d''axe arrière de 12 x 142 mm, 12 x 148 mm et 12 x 157 mm offrent deux avantages principaux aux cyclistes Kona : le diamètre de 12 mm de l''axe arrière garantit une stabilité maximale du moyeu arrière et du cadre, tandis que le diamètre extérieur de 142/148/157 mm du moyeu garantit que la roue est rapide et correctement positionnée dans le cadre avant que l''axe arrière puisse être utilisé. A partir de 2016, le standard 12x148 mm existe en mix, surtout sur le nouvel alliage Honzos. Le 12x148 offre plus d''espace pour les pneus au niveau des bases, tandis que la roue arrière est plus stable et plus résistante qu''un axe de 12 x 142 mm. KONA 6061 Aluminium : Les alliages d''aluminium Kona 7005 et 6061 sont largement utilisés pour les vélos de montagne et d''asphalte. Un alliage léger robuste et durable, à la fois le Kona 7005 et le 6061, offre des performances fantastiques et fiables qui permettent des milliers de trajets. Une grande partie de notre tube 7005/6061 est conifiée et/ou façonnée, ce qui signifie que l''épaisseur de la paroi du tube peut être augmentée ou diminuée, mais aussi façonnée, ce qui nous permet d''ajuster finement la résistance et les caractéristiques de conduite d''un cadre donné en fonction de l''application prévue. Tube à tête conique : Une plus grande circonférence sous le tube de direction répartit mieux la force d''impact, prolonge la durée de vie des roulements du jeu de direction et élimine le choc de freinage tout en fournissant une performance de direction sûre.La force inhérente de son design triangulaire signifie également une position de conduite plus forte et un meilleur équilibre, ce qui donne au conducteur plus de contrôle sur les terrains accidentés.', 'Kona', 'Kona', 'kona-honzo.jpg', 10),
('Cube Reaction Hybrid Performance 500 Allroad', 2749.00, 2, 3, 'Aluminium', 'Cube Reaction Hybrid Performance 500 Allroad Trapez - L''entrée de gamme avantageuse dans le monde des électriques Cube. Le vélo le plus abordable de la série "Reaction Hybrid" est un vélo formidable pour les randonnées en forêt. Les excursions dans la vie quotidienne sont particulièrement faciles avec ce vélo, car le cadre trapézoïdal avec un accès plus bas facilite la montée et la descente. De plus, ce modèle est doté d''un équipement "Allroad" - grâce à des garde-boue, une béquille et un système d''éclairage puissant, il brille sur les chemins forestiers et dans la circulation urbaine. Un vrai touche-à-tout sur toutes les routes ! Dans la gamme Cube Reaction, le terme "Performance" désigne les variantes les moins chères. Ils ont beaucoup en commun avec les modèles haut de gamme. Un cadre de haute qualité combiné à un moteur Bosch garantit un plaisir de conduite énorme pour une somme modique. Ce n''est que si tu as absolument besoin des plus grosses batteries pour de longues randonnées vallonnées ou d''un moteur particulièrement puissant pour des montées très raides que tu devrais regarder les autres modèles. Le Cube Reaction Hybrid est un électrique. Mais en même temps, c''est peut-être la plateforme la plus transformable que Cube propose. La large gamme de modèles couvre tous les domaines d''utilisation, des promenades sportives en fin de journée dans la forêt aux longues randonnées en montagne, en passant par le quotidien en ville. Avec quelques adaptations, tu peux transformer n''importe quel vélo d''un véhicule de tous les jours en un bolide sportif pour la forêt, si tes besoins devaient changer un jour. Tous les modèles brillent par leur polyvalence et leur confort. Quel que soit le vélo pour lequel tu optes, le moteur est toujours issu de la série Performance de Bosch avec le système Bosch Smart. La référence dans le domaine des électriques te pousse vigoureusement non seulement dans la forêt, mais aussi dans toutes les situations de la vie. L''ensemble comprend toujours des pneus larges (et donc confortables), des freins hydrauliques puissants et une fourche suspendue. Construction du cadre : Le Cube Reaction Hybrid redéfinit la forme fondamentale du cadre du. Les hardtails - des dont seule la roue avant est suspendue - sont appréciés pour leur maniabilité, leur faible entretien et leur longue durée de vie. Le Reaction Hybrid a en outre des astuces supplémentaires à proposer. Les cadres de taille S sont livrés avec des roues plus petites de 27 pouces afin de donner à ces vélos un comportement similaire à celui des grandes tailles avec des roues de pouces. De toute façon, Cube a déjà investi beaucoup d''efforts depuis des années dans le cadre de la "Agile Ride Geometry" pour donner à ses vélos une trajectoire droite stable et malgré tout un comportement ludique dans les virages. Système intelligent Bosch : Ces vélos électriques sont intelligents - du moins en interaction avec l''application "Bosch E-Bike Flow" sur ton smartphone. Elle peut désormais faire beaucoup de choses pour lesquelles tu avais besoin d''un rendez-vous de service auparavant. Cela commence par des statistiques très simples comme la distance parcourue, l''état de la batterie ou la prochaine échéance d''entretien, mais cela ne s''arrête pas là. Tu peux par exemple adapter les niveaux d''assistance (dans le cadre des réglementations légales bien sûr) ou installer des mises à jour logicielles. De même, tu peux utiliser ton téléphone comme un très grand écran, te faire guider jusqu''à ta destination, enregistrer tes trajets et les synchroniser directement avec des applications de fitness.', 'Cube', 'Cube', 'cube-reaction-hybrid-performance-500-allroad-trapeze.jpg', 10),
('Ridley Bikes Helium Disc 105', 3199.00, 3, 8, 'Carbone', 'Le vélo de route performant Helium Disc contient toutes les qualités cyclistes sans précédent et la superbe technologie qui équipent le vélo haut de gamme Helium SLX Disc, mais à un prix nettement inférieur. Le vélo de route Helium Disc incorpore la forme unique du tube ovale qui équilibre parfaitement la rigidité, le poids et le confort. De plus, tous les câbles sont entièrement intégrés dans l''Helium grâce à la technologie F-Steerer. Cela lui confère un look épuré qui ne nécessite aucun entretien. Ce que vous sentirez, c''est la légèreté, la réactivité, la rigidité et le confort du vélo, du premier au dernier coup de pédale. Ce que vous ne sentirez pas, ce sont les 120 grammes supplémentaires sur le cadre (car il est fabriqué en Essential Carbon), ce qui lui permet d''être beaucoup plus abordable que son grand frère, le SLX. À propos de la famille Helium : Les vélos Helium sont les meilleurs vélos de route polyvalents pour les cyclistes les plus exigeants. Ces machines hautes performances sont incroyablement rigides et résistantes, tout en étant ultralégères, ce qui leur permet de grimper des pentes incroyablement raides. Ils se comportent également comme un rêve lorsqu''ils s''envolent à toute vitesse dans les descentes difficiles. C''est ce qui en fait le cadre préféré des cyclistes professionnels de Lotto Soudal. Bien que leurs tubes ronds et classiques puissent offrir le meilleur équilibre entre poids et rigidité et entre réactivité et confort, cela ne les aide certainement pas à se démarquer de la foule. Ce qui leur permet d''obtenir des notes de performance incroyables dans tous les tests de vélos, ce sont leurs caractéristiques de conduite sublimes. En résumé, ce vélo élève instantanément le niveau de cyclisme de chaque cycliste - à tous points de vue.', 'Ridley', 'Ridley', 'ridley-bikes-helium-disc-105.jpg', 10),
('Cube Aerium C:68 SL Low', 6499.00, 4, 8, 'Carbone', 'Il n''y a probablement pas de vélo plus rapide dans le cirque du triathon que l''Aerium C:68 SL. La vitesse et les performances élevées sont dues à son aérodynamique innovante et à la sélection minutieuse de ses composants haut de gamme. Grâce au changement de vitesse radio piloté Sram Force AXS à 12 rapports, vous pouvez passer d''une vitesse à l''autre en douceur, d''une simple pression du doigt. Et parce qu''avec une telle poussée vers l''avant en forme de flèche, le contrôle, la puissance de freinage et l''adhérence sont essentiels, Cube a donné au volant Fulcrum Aero Racing 44 roues avec des pneus Schwalbe Pro One TLE et des freins sur jante RT Aero de Magura. Au fait, le système de cockpit CUBE C:68 est disponible en version haute et basse - et avec un système d''hydratation optimisé. Tout en vue, tout sous contrôle !', 'Cube', 'Cube', 'cube-aerium-c68-sl-low.jpg', 0),
('Mongoose California Special', 599.00, 1, 7, 'Acier', 'Les fans du classique Mongoose peuvent se réjouir - le vélo BMX California Special est de retour ! Basée sur le design original de 1983, la nouvelle California Special est géniale pour faire tourner les têtes dans le quartier ou sur la piste. Il est doté d''un cadre en acier Hi-Ten de Mongoose, qui s''appuie sur la géométrie originale d''une légende pour offrir des performances et une durabilité supérieures. La transmission singlespeed est facile à utiliser et à entretenir, tandis que le système de freinage DiaCompe MX fournit une force de freinage super rapide et fiable. De plus, les jantes en aluminium percées uniques de Mongoose Pro Class offrent des performances qui ne vous alourdissent pas. Ne manquez pas votre chance de profiter d''un tour sur la légendaire California Special de Mongoose. ', 'Mongoose', 'Mongoose', 'mongoose-california-special.jpg', 1),
('Cube Nature Pro', 949.00, 1, 9, 'Aluminium', ' Si vous aimez sortir des sentiers battus avec votre vélo, vous allez adorer le Nature Pro. L''une des raisons en est la large gamme de rapports de la transmission Shimano 3x10 vitesses, facile à utiliser avec un dérailleur XT super fiable sur la roue arrière. Il suffit d''un simple clic pour obtenir la bonne vitesse pour chaque montée, même la plus raide. Le confort de conduite est également élevé et durable grâce à la fourche suspendue Suntour et aux pneus Schwalbe roulant en douceur. Enfin, et surtout, les puissants freins à disque hydrauliques de Shimano fournissent une force de freinage absolument fiable et donc une sécurité, indépendamment des conditions météorologiques ou du terrain. Conclusion : Tout ce dont vous avez besoin est là – la marque a délibérément renoncé aux fioritures inutiles. Plus un vélo est léger, meilleure est sa tenue de route – c''est pourquoi le cadre Nature est également composé de tubes en aluminium à double confinement. L''avantage : un faible poids, sans perdre la stabilité et la longévité. De plus, il laisse suffisamment de place pour des pneus jusqu''à 50 mm de large pour un meilleur confort de conduite et possède un tube de direction conique pour une précision de direction optimale. En plus des raccords de tubes conçus selon le procédé Smooth Welding, d''élégants points de connexion pour le porte-bagages et les garde-boue soulignent l''allure gracieuse et permettent de modifier et d''adapter facilement le vélo aux besoins individuels. Et le fait que le châssis – comme d''ailleurs tous les cadres de CUBE – ait non seulement passé tous les tests de sécurité avec brio, mais qu''il ait même dépassé les exigences, va presque de soi. Vous êtes ainsi encore plus détendu sur la route – et ce, plus longtemps ! ', 'Cube', 'Cube', 'cube-nature-pro.jpg', 10),
('Ortler Detroit Cargo Steel Balançoire', 399.00, 3, 4, 'Acier', 'Ortler Detroit EQ Cargo Wave vitesses - Un cargo cruiser au look rétro Le Ortler Detroit EQ Cargo Bike allie style et fonctionnalité au quotidien : Un classique de la ville en acier avec un accès bas, dans lequel tu glisses souverainement dans une position assise confortablement droite et où tu as tout sous les yeux. La transmission Shimano Tourney à six vitesses, qui a fait ses preuves, t''aide à varier ton rythme et à trouver le bon rapport pour chaque situation en ville, ce qui est aussi particulièrement important si tu as chargé une bonne cargaison sur les porte-bagages avant et arrière. En effet, ce vélo n''est pas seulement beau, il peut aussi conduire tes courses à travers la ville. Le système d''éclairage de style rétro est bien entendu homologué par le StVZO, les garde-boue et le protège-chaîne de la même couleur que le cadre complètent le vélo en termes de style et d''équipement complet. Grâce à l''enjambement bas et à la grande plage de réglage du guidon et de la selle, les cyclistes* mesurant entre 1,55 et 1,85 se déplacent confortablement avec le cadre Ortler Detroit EQ taille Unisize.', 'Ortler', 'Ortler', 'ortler-detroit-cargo-steel-swing.jpg', 10),
('Wethepeople Arcade', 629.99, 1, 7, 'Acier', 'L''Arcade a été relooké et dispose désormais d''une base de chaîne super-réactive de 12 pouces 75-Zoll-Kettenstrebe, parfaite pour les cyclistes de route techniques ou les jeunes cyclistes qui veulent un vélo facile à manier et sur lequel ils peuvent progresser rapidement.L''Acrade roule maintenant sur des jantes Valon super larges de 36 mm de SALT et des moyeux étanches avec des pneus SALTPLUS BURN, ce qui donne une combinaison de roues et de pneus incroyablement fiable. Disponible en option 20,5" ou 21" plus longue, l''Arcade offre aux cyclistes plus grands ou plus âgés la possibilité de rouler sur l''un des vélos les plus populaires de la gamme Wethepeople. ', 'Wethepeople', 'Wethepeople', 'wethepeople-arcade.jpg', 10),
('Winora Domingo 21 Diamant', 629.00, 4, 5, 'Aluminium', 'Le design classique intemporel, le très bon rapport qualité-prix et la qualité supérieure font des modèles Domingo le choix parfait pour les cyclistes qui aiment pédaler eux-mêmes. Que ce soit pour faire la navette, pour les loisirs ou pour rester en forme - avec le WINORA Domingo 21, tu obtiens un compagnon polyvalent, prêt à tout moment pour de longues randonnées et qui t''emmène souverainement à travers la ville. La combinaison d''un cadre en aluminium léger et de haute qualité, d''une fourche suspendue Suntour et d''un dérailleur Shimano à vitesses garantit dynamisme et confort, même sur les parcours les plus accidentés.', 'Winora', 'Winora', 'winora-domingo-21-diamond.jpg', 10),
('Vitus Escarpe 290 AMP', 6199.00, 3, 2, 'Carbone', 'Lumière tamisée de la forêt sur des sentiers chauds et poussiéreux. Le bruit des pneus qui bruissent sur les crêtes, qui se faufilent habilement dans un jardin de pierres et le bourdonnement d''une roue libre heureuse. Les yeux sont fixés sur le chemin devant toi. Tu es concentré, mais c''est facile. Sur le Vitus Escarpe 29 CRX entièrement en carbone, il n''y a pas de distractions. Tout en confiance et en contrôle total.Mais la vie n''est pas une séance photo, alors soyons réalistes. Alternance de hors-cambre, de hors-piste mouvementé et de virages délavés, de racines glissantes et de "la montée" pour revenir au point de départ du sentier. Cela n''a pas d''importance. L''Escarpe est équilibrée et parfaitement balancée pour couler avec toi, peu importe où le trail te mène. Toi et le vélo chantez sur la même partition. Tu veux un vélo qui te donne confiance dans les descentes techniques et qui te fait sourire au lieu de te faire grincer des dents. Tu veux un vélo qui maintient la vitesse et qui s''engage vivement dans les montées pour garder tes jambes fraîches pour une autre course. Ils veulent un poids léger et des performances élevées. C''est ça. Que tu freines fort, que tu donnes plus de puissance ou que tu affrontes une descente sinueuse, ton centre de gravité est rarement constant, la clé de tout le système est donc l''efficacité. Pour faire face à la nature dynamique du trail, l''Escarpe reste prévisible et cohérente, ce qui te permet de rester décontracté. Ici, pas de sensations fortes. La cinématique de la suspension a été améliorée par rapport à la plateforme précédente afin de réduire davantage l''impact des rebonds de pédales et de diminuer la dureté des petites bosses et des vibrations du trail qui consomment ton énergie et réduisent la vitesse. Plus de fluidité signifie plus de vitesse pour plus longtemps. Grâce à un flip-chip réglable qui relève le boîtier de pédalier de 6 mm et augmente l''angle de la tête de direction, le set-up peut être adapté de manière optimale à tes habitudes et conditions de conduite. De plus, la géométrie et les performances sont optimisées sur toute la gamme de tailles, de sorte que, que tu roules en S ou en XL, tu n''as pas à faire de compromis sur les sensations de conduite. Sur les sentiers, il y a suffisamment à penser sans avoir à se soucier de la manière dont le vélo va réagir au prochain virage ou au prochain obstacle. Il faut le savoir. Il devrait faire ce que tu lui demandes. Pas de discussion ni de lutte. Sur l''escarpe, tu n''as pas besoin de compenser ou de faire des compromis. Tu n''as pas besoin d''adapter ton style de conduite. Conduis. Concentre-toi simplement sur le fait de t''amuser. Le carbone en première ligne : Lors du développement des nouvelles plateformes Sommet et Escarpe, Vitus a décidé très tôt de mettre l''accent sur un triangle avant uniquement en carbone avec un triangle arrière en aluminium. Il en résulte un mélange parfait de rigidité et de souplesse. Un plus grand volume de tubes dans le triangle avant améliore la rigidité et assure un meilleur suivi et une meilleure stabilité sur toute la gamme de tailles. Géométrie mise à jour : Les vélos ont une géométrie actualisée pour donner une sensation de conduite qui inspire confiance. Les principaux changements sont un angle de tête de direction plus plat et une distance de pédalier réduite. Vitus a également rendu l''angle effectif du tube de selle plus raide et l''a rendu de plus en plus raide au fur et à mesure que la taille augmentait. Cela permet de garantir que chaque taille de cadre a une position de selle fléchie optimale, sans compromis. Lors de la mesure de la hauteur de la selle en position de selle, la position de la selle par rapport au pédalier a été étudiée afin de s''assurer que l''on a une position de pédalage optimale lorsque la selle est affaissée. La raison pour laquelle l''angle d''assise est plus raide sur les grandes tailles de cadre était de s''assurer que la selle n''était pas trop en arrière du pédalier. Flip Chip réglable : L''escarpe est livrée avec un flip chip réglable qui permet d''adapter la géométrie selon les besoins. Vitus a ajusté et optimisé l''angle de la tête de direction et la chute du pédalier en fonction du réglage "Low". Le réglage "High" permet toutefois d''augmenter l''angle de la tête de direction de 0,5 degré et de relever le boîtier de pédalier de 6 mm. Tu as ainsi la possibilité d''adapter la conduite à chaque terrain.', 'Vitus', 'Vitus', 'vitus-escarpe-29-amp-intl-vitus.jpg', 4),
('Kona Dew-E DL', 3519.00, 4, 3, 'Aluminium', 'Les navetteurs aiment le Dew-E DL pour son design élégant et parce qu''il est tout simplement amusant à conduire. Le cadre en aluminium est équipé d''une fourche Kona Rove Verso Full Carbon Flat Mount Disc. La transmission à vitesses s''harmonise parfaitement avec le moteur Shimano à plat et la batterie intégrée. Des garde-boue solides en aluminium et un éclairage te permettent de rester au sec et bien visible pendant ton trajet. De puissants freins à disque hydrauliques et des rotors de 160 mm te stoppent en un clin d''œil, même par temps humide, et les pneus increvables de 650x47c-Reifen te permettent de progresser aussi bien sur l''asphalte que sur les chemins de terre. C''est le vélo électrique de banlieue que vous cherchiez depuis longtemps !', 'Kona', 'Kona', 'kona-dew-e-dl.jpg', 9),
('Ridley Bikes Kanzo A Rival 1', 2299.00, 1, 1, 'Aluminium', 'Le Kanzo Aluminium est un vélo incroyablement polyvalent. Avec les pare-buffles montés, tu disposes d''un vélo de ville stable et idéal pour un trajet quotidien agréable vers le travail. Chausse des pneus tout-terrain pour t''amuser en dehors des sentiers battus. Le vélo Kanzo A Allroad dispose d''une grande liberté de mouvement des pneus et de nombreux œillets de cadre, ce qui le rend idéal pour transporter des bagages lors de randonnées à vélo. En route pour la nature et profitez-en ! Ce kanzo te soutiendra toujours. Grâce à sa géométrie parfaite, le confort et la stabilité sont parfaitement combinés. Avec ce vélo gravel économique, tu as aussi ce qu''il te faut sur les terrains de gravel. Sors de la rue et fais-en toi-même l''expérience !', 'Ridley', 'Ridley', 'ridley-bikes-kanzo-a-rival-1.jpg', 5);
'''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:600000$828ij7RCZN24IWfq$3dbd14ea15999e9f5e340fe88278a45c1f41901ee6b2f56f320bf1fa6adb933d',
    'ROLE_admin','admin'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:600000$ik00jnCw52CsLSlr$9ac8f694a800bca6ee25de2ea2db9e5e0dac3f8b25b47336e8f4ef9b3de189f4',
    'ROLE_client','client'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:600000$3YgdGN0QUT1jjZVN$baa9787abd4decedc328ed56d86939ce816c756ff6d94f4e4191ffc9bf357348',
    'ROLE_client','client2');'''
    mycursor.execute(sql)

    sql = '''
INSERT INTO etat(libelle_etat) VALUES
('en attente'),
('expedié'),
('validé'),
('confirmé');'''
    mycursor.execute(sql)

    sql = '''
INSERT INTO commande (date_achat, utilisateur_id, etat_id) VALUES
('2024-01-27 14:45:50', 2, 1),
('2024-01-28 20:00:00', 3, 1),
('2024-01-01 8:15:30', 3, 1),
('2024-02-10 12:30:00', 2, 1),
('2024-02-12 18:45:15', 2, 2),
('2024-02-15 09:00:00', 2, 2);'''
    mycursor.execute(sql)

    sql = '''
INSERT INTO ligne_commande (commande_id, velo_id, prix, quantite_commande) VALUES
(1, 10, 1599.00, 2),
(1, 21, 2299.00, 1),
(2, 4, 1299.00, 3),
(3, 3,3099.00, 4),
(3, 13, 6499.00, 1),
(3, 18, 629.00, 2),
(4, 5, 5799.00, 2),
(5, 16, 399.00, 2),
(5, 14, 599.00, 1),
(6, 12, 6499.00, 3);'''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')