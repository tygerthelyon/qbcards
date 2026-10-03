# -*- coding: utf-8 -*-
"""images.py -- the pictures History v2 uses: key -> (media filename, caption, source page).

Every file is in media/, already resized (at most 1280 px on the long side). Each was looked at on a
contact sheet before it went in, to check it shows the card's answer and doesn't print the answer
where a front would show it. Picture-card fronts never show the caption.
Sources: Wikimedia Commons / Wikipedia lead images, public domain or CC (see the source page).
"""

IMAGES = {
    "pangu": ("hist2-pangu.jpg", "Pangu, from the Ming encyclopedia <i>Sancai Tuhui</i> (1609)",
              "https://commons.wikimedia.org/wiki/File:Pangu.jpg"),
    "nuwa_fuxi": ("hist2-nuwa-fuxi.jpg", "Fuxi and Nüwa with intertwined snake tails, holding a set square and a "
                  "compass; silk painting from Astana, Turfan (Tang dynasty)",
                  "https://commons.wikimedia.org/wiki/File:Anonymous-Fuxi_and_N%C3%BCwa.jpg"),
    "nuwa_mend": ("hist2-nuwa-mend.jpg", "Nüwa holding up a stone to mend the sky; temple relief, Ping Sien Si, Malaysia",
                  "https://commons.wikimedia.org/wiki/File:Ping_Sien_Si_-_065_Nu_Wa_Niang_Niang_(16140351273).jpg"),
    "shennong": ("hist2-shennong.jpg", "Shennong tasting herbs; Guo Xu, album leaf dated 1503 (Ming)",
                 "https://commons.wikimedia.org/wiki/File:Guo_Xu_album_dated_1503_(2).jpg"),
    "huangdi": ("hist2-huangdi.jpg", "The Yellow Emperor; from the album <i>Portraits of Famous Men</i>",
                "https://commons.wikimedia.org/wiki/File:Portraits_of_Famous_Men_-_Yellow_Emperor_(Huangdi).jpg"),
    "jade_emperor": ("hist2-jade-emperor.jpg", "The Jade Emperor enthroned; Qing devotional painting",
                     "https://commons.wikimedia.org/wiki/File:%E7%8E%89%E7%9A%87%E5%A4%A7%E5%B8%9D%E7%95%AB%E5%83%8F.jpg"),
    "change": ("hist2-change.jpg", "<i>The Moon Goddess Chang'e</i>, after Tang Yin (Ming)",
               "https://commons.wikimedia.org/wiki/File:The_Moon_Goddess_Chang_E_-_Unidentified_artist,_after_Tang_Yin.jpg"),
    "houyi": ("hist2-houyi.jpg", "Hou Yi shooting at the suns; Xiao Yuncong (17th century)",
              "https://commons.wikimedia.org/wiki/File:Houyi_Shooting_an_Arrow,_Xiao_Yuncong.gif"),
    "xiwangmu": ("hist2-xiwangmu.jpg", "The Queen Mother of the West; detail of a painting by Xie Wenli",
                 "https://commons.wikimedia.org/wiki/File:Detail_of_Xie_Wenli%27s_painting_of_Xi_Wangmu.jpg"),
    "cowherd": ("hist2-cowherd.jpg", "The Cowherd and the Weaver Girl meeting on the magpie bridge; festival lantern",
                "https://commons.wikimedia.org/wiki/File:The_Magpie_Bridge.jpg"),
    "kitchen_god": ("hist2-kitchen-god.jpg", "Zao Jun, the Kitchen God, with attendants; New Year print",
                    "https://commons.wikimedia.org/wiki/File:Zao_Jun_-_The_Kitchen_God_-_-_Project_Gutenberg_eText_15250.jpg"),
    "mazu": ("hist2-mazu.jpg", "Mazu enthroned; carved and gilded wood, late Qing",
             "https://commons.wikimedia.org/wiki/File:Wood_Statue_of_Mazu_Late_19th_century_CE_Qing_Dynasty_(1644-1911_CE)_China.jpg"),
    "yu": ("hist2-yu.jpg", "Yu the Great; hanging scroll attributed to Ma Lin (Song), National Palace Museum",
           "https://commons.wikimedia.org/wiki/File:King_Yu_of_Xia.jpg"),
    "four_symbols": ("hist2-four-symbols.jpg", "The Four Symbols on Han roof-tile ends: Black Tortoise, Azure Dragon "
                     "(top); White Tiger, Vermilion Bird (bottom)", "https://commons.wikimedia.org/wiki/File:Four_Symbols.svg"),
    "peach_garden": ("hist2-peach-garden.jpg", "The Oath of the Peach Garden; woodblock illustration to <i>Romance of "
                     "the Three Kingdoms</i> (Ming)", "https://commons.wikimedia.org/wiki/File:Peach_garden_ceremony.jpg"),
    "zhuge": ("hist2-zhuge.jpg", "Zhuge Liang; Ming portrait (Nanxun Hall album)",
              "https://commons.wikimedia.org/wiki/File:%E6%98%8E%E4%BA%BA%E7%BB%98_%E3%80%8A%E8%AF%B8%E8%91%9B%E4%BA%AE%E5%83%8F%E3%80%8B%EF%BC%88%E5%8D%97%E8%96%B0%E6%AE%BF%E6%9C%AC%EF%BC%89.jpg"),
    "caocao": ("hist2-caocao.jpg", "Cao Cao; modern bronze bust in a museum display",
               "https://commons.wikimedia.org/wiki/File:Statue_of_Cao_Cao.jpg"),
    "guanyu": ("hist2-guanyu.jpg", "Shang Xi, <i>Guan Yu Captures General Pang De</i> (Ming, early 15th century): Guan Yu, red-faced, "
               "sits in green", "https://commons.wikimedia.org/wiki/File:Shang_Xi,_Guan_Yu_Captures_General_Pang_De2.JPG"),
    "red_cliffs": ("hist2-red-cliffs.jpg", "The cliff at Chibi, Hubei, carved with the characters 赤壁 ('Red Cliffs')",
                   "https://commons.wikimedia.org/wiki/File:Chibi.jpg"),
    "wusong": ("hist2-wusong.jpg", "Wu Song killing the tiger; painting in the Long Corridor, Summer Palace, Beijing",
               "https://commons.wikimedia.org/wiki/File:Wu_Song_Water_Margin.jpg"),
    "wukong": ("hist2-wukong.jpg", "Sun Wukong with his staff; woodcut illustration to <i>Journey to the West</i>",
               "https://commons.wikimedia.org/wiki/File:Xiyou.PNG"),
    "daiyu": ("hist2-daiyu.jpg", "Lin Daiyu burying fallen flowers; Qing album leaf",
              "https://commons.wikimedia.org/wiki/File:Lin_Daiyu_Burying_Flowers.png"),
    "eight_immortals": ("hist2-eight-immortals.jpg", "The Eight Immortals at the Queen Mother of the West's gathering; "
                        "detail of a Ming painting (British Museum)",
                        "https://commons.wikimedia.org/wiki/File:Detail_of_%E7%91%A4%E6%B1%A0%E4%BB%99%E5%8A%87%E5%9C%96_(Gathering_of_Immortals)_Ming_dynasty_painting_British_Museum.jpg"),
    "jttw": ("hist2-jttw.jpg", "The opening page of a Ming edition of <i>Journey to the West</i>",
             "https://commons.wikimedia.org/wiki/File:Evl53201b_pic.jpg"),
}
