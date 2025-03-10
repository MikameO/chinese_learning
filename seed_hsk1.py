import os
from app import create_app, db
from models import Character

# All 150 HSK 1 words (both single- and multi-character entries).
# Short definitions are used here for brevity.
HSK1_WORDS = [
    {"hanzi": "爱",      "pinyin": "ài",         "meaning": "love"},
    {"hanzi": "八",      "pinyin": "bā",         "meaning": "eight"},
    {"hanzi": "爸爸",    "pinyin": "bàba",       "meaning": "dad"},
    {"hanzi": "杯子",    "pinyin": "bēizi",      "meaning": "cup"},
    {"hanzi": "北京",    "pinyin": "Běijīng",    "meaning": "Beijing"},
    {"hanzi": "本",      "pinyin": "běn",        "meaning": "measure word (books)"},
    {"hanzi": "不",      "pinyin": "bù",         "meaning": "no; not"},
    {"hanzi": "菜",      "pinyin": "cài",        "meaning": "dish"},
    {"hanzi": "茶",      "pinyin": "chá",        "meaning": "tea"},
    {"hanzi": "吃",      "pinyin": "chī",        "meaning": "to eat"},
    {"hanzi": "出租车",  "pinyin": "chūzūchē",   "meaning": "taxi"},
    {"hanzi": "打电话",  "pinyin": "dǎ diànhuà","meaning": "to call"},
    {"hanzi": "大",      "pinyin": "dà",         "meaning": "big"},
    {"hanzi": "的",      "pinyin": "de",         "meaning": "possession particle"},
    {"hanzi": "点",      "pinyin": "diǎn",       "meaning": "o'clock"},
    {"hanzi": "电脑",    "pinyin": "diànnǎo",    "meaning": "computer"},
    {"hanzi": "电视",    "pinyin": "diànshì",    "meaning": "TV"},
    {"hanzi": "电影",    "pinyin": "diànyǐng",   "meaning": "movie"},
    {"hanzi": "东西",    "pinyin": "dōngxi",     "meaning": "thing"},
    {"hanzi": "都",      "pinyin": "dōu",        "meaning": "all"},
    {"hanzi": "读",      "pinyin": "dú",         "meaning": "to read"},
    {"hanzi": "对不起",  "pinyin": "duìbuqǐ",    "meaning": "sorry"},
    {"hanzi": "多",      "pinyin": "duō",        "meaning": "many"},
    {"hanzi": "多少",    "pinyin": "duōshao",    "meaning": "how many"},
    {"hanzi": "儿子",    "pinyin": "érzi",       "meaning": "son"},
    {"hanzi": "二",      "pinyin": "èr",         "meaning": "two"},
    {"hanzi": "饭馆",    "pinyin": "fànguǎn",    "meaning": "restaurant"},
    {"hanzi": "飞机",    "pinyin": "fēijī",      "meaning": "airplane"},
    {"hanzi": "分钟",    "pinyin": "fēnzhōng",   "meaning": "minute"},
    {"hanzi": "高兴",    "pinyin": "gāoxìng",    "meaning": "happy"},
    {"hanzi": "个",      "pinyin": "gè",         "meaning": "measure word"},
    {"hanzi": "工作",    "pinyin": "gōngzuò",    "meaning": "work"},
    {"hanzi": "汉语",    "pinyin": "Hànyǔ",      "meaning": "Chinese language"},
    {"hanzi": "好",      "pinyin": "hǎo",        "meaning": "good"},
    {"hanzi": "号",      "pinyin": "hào",        "meaning": "day; number"},
    {"hanzi": "喝",      "pinyin": "hē",         "meaning": "to drink"},
    {"hanzi": "和",      "pinyin": "hé",         "meaning": "and"},
    {"hanzi": "很",      "pinyin": "hěn",        "meaning": "very"},
    {"hanzi": "后面",    "pinyin": "hòumian",     "meaning": "behind"},
    {"hanzi": "回",      "pinyin": "huí",        "meaning": "to return"},
    {"hanzi": "会",      "pinyin": "huì",        "meaning": "can; able to"},
    {"hanzi": "火车站",  "pinyin": "huǒchēzhàn", "meaning": "train station"},
    {"hanzi": "几",      "pinyin": "jǐ",         "meaning": "how many"},
    {"hanzi": "家",      "pinyin": "jiā",        "meaning": "home; family"},
    {"hanzi": "叫",      "pinyin": "jiào",       "meaning": "to be called"},
    {"hanzi": "今天",    "pinyin": "jīntiān",     "meaning": "today"},
    {"hanzi": "九",      "pinyin": "jiǔ",        "meaning": "nine"},
    {"hanzi": "开",      "pinyin": "kāi",        "meaning": "to open; to start"},
    {"hanzi": "看",      "pinyin": "kàn",        "meaning": "to see; to watch"},
    {"hanzi": "看见",    "pinyin": "kànjiàn",    "meaning": "to see"},
    {"hanzi": "块",      "pinyin": "kuài",       "meaning": "Yuan; piece"},
    {"hanzi": "来",      "pinyin": "lái",        "meaning": "to come"},
    {"hanzi": "老师",    "pinyin": "lǎoshī",     "meaning": "teacher"},
    {"hanzi": "了",      "pinyin": "le",         "meaning": "completed action"},
    {"hanzi": "冷",      "pinyin": "lěng",       "meaning": "cold"},
    {"hanzi": "里",      "pinyin": "lǐ",         "meaning": "inside"},
    {"hanzi": "零",      "pinyin": "líng",       "meaning": "zero"},
    {"hanzi": "六",      "pinyin": "liù",        "meaning": "six"},
    {"hanzi": "妈妈",    "pinyin": "māma",       "meaning": "mom"},
    {"hanzi": "吗",      "pinyin": "ma",         "meaning": "question particle"},
    {"hanzi": "买",      "pinyin": "mǎi",        "meaning": "to buy"},
    {"hanzi": "卖",      "pinyin": "mài",        "meaning": "to sell"},
    {"hanzi": "猫",      "pinyin": "māo",        "meaning": "cat"},
    {"hanzi": "没",      "pinyin": "méi",        "meaning": "not have"},
    {"hanzi": "没关系",  "pinyin": "méi guānxi", "meaning": "it's okay"},
    {"hanzi": "米饭",    "pinyin": "mǐfàn",      "meaning": "cooked rice"},
    {"hanzi": "明天",    "pinyin": "míngtiān",   "meaning": "tomorrow"},
    {"hanzi": "名字",    "pinyin": "míngzi",     "meaning": "name"},
    {"hanzi": "哪",      "pinyin": "nǎ",         "meaning": "which"},
    {"hanzi": "哪儿",    "pinyin": "nǎr",        "meaning": "where"},
    {"hanzi": "那",      "pinyin": "nà",         "meaning": "that"},
    {"hanzi": "那儿",    "pinyin": "nàr",        "meaning": "there"},
    {"hanzi": "呢",      "pinyin": "ne",         "meaning": "question particle"},
    {"hanzi": "能",      "pinyin": "néng",       "meaning": "can; be able to"},
    {"hanzi": "你",      "pinyin": "nǐ",         "meaning": "you"},
    {"hanzi": "年",      "pinyin": "nián",       "meaning": "year"},
    {"hanzi": "女儿",    "pinyin": "nǚ'ér",      "meaning": "daughter"},
    {"hanzi": "朋友",    "pinyin": "péngyou",    "meaning": "friend"},
    {"hanzi": "漂亮",    "pinyin": "piàoliang",  "meaning": "pretty"},
    {"hanzi": "苹果",    "pinyin": "píngguǒ",    "meaning": "apple"},
    {"hanzi": "七",      "pinyin": "qī",         "meaning": "seven"},
    {"hanzi": "前面",    "pinyin": "qiánmian",   "meaning": "front"},
    {"hanzi": "钱",      "pinyin": "qián",       "meaning": "money"},
    {"hanzi": "请",      "pinyin": "qǐng",       "meaning": "please"},
    {"hanzi": "去",      "pinyin": "qù",         "meaning": "to go"},
    {"hanzi": "热",      "pinyin": "rè",         "meaning": "hot"},
    {"hanzi": "人",      "pinyin": "rén",        "meaning": "person"},
    {"hanzi": "认识",    "pinyin": "rènshi",     "meaning": "to know (somebody)"},
    {"hanzi": "三",      "pinyin": "sān",        "meaning": "three"},
    {"hanzi": "商店",    "pinyin": "shāngdiàn",  "meaning": "store"},
    {"hanzi": "上",      "pinyin": "shàng",      "meaning": "up"},
    {"hanzi": "上午",    "pinyin": "shàngwǔ",    "meaning": "morning"},
    {"hanzi": "少",      "pinyin": "shǎo",       "meaning": "few"},
    {"hanzi": "谁",      "pinyin": "shéi",       "meaning": "who"},
    {"hanzi": "什么",    "pinyin": "shénme",     "meaning": "what"},
    {"hanzi": "十",      "pinyin": "shí",        "meaning": "ten"},
    {"hanzi": "时候",    "pinyin": "shíhou",     "meaning": "time"},
    {"hanzi": "是",      "pinyin": "shì",        "meaning": "to be"},
    {"hanzi": "书",      "pinyin": "shū",        "meaning": "book"},
    {"hanzi": "水",      "pinyin": "shuǐ",       "meaning": "water"},
    {"hanzi": "水果",    "pinyin": "shuǐguǒ",    "meaning": "fruit"},
    {"hanzi": "睡觉",    "pinyin": "shuìjiào",   "meaning": "to sleep"},
    {"hanzi": "说",      "pinyin": "shuō",       "meaning": "to speak"},
    {"hanzi": "四",      "pinyin": "sì",         "meaning": "four"},
    {"hanzi": "岁",      "pinyin": "suì",        "meaning": "years old"},
    {"hanzi": "他",      "pinyin": "tā",         "meaning": "he; him"},
    {"hanzi": "她",      "pinyin": "tā",         "meaning": "she; her"},
    {"hanzi": "太",      "pinyin": "tài",        "meaning": "too"},
    {"hanzi": "天气",    "pinyin": "tiānqì",     "meaning": "weather"},
    {"hanzi": "听",      "pinyin": "tīng",       "meaning": "to listen"},
    {"hanzi": "同学",    "pinyin": "tóngxué",    "meaning": "classmate"},
    {"hanzi": "喂",      "pinyin": "wèi (wéi)",  "meaning": "hello (on phone)"},
    {"hanzi": "我",      "pinyin": "wǒ",         "meaning": "I; me"},
    {"hanzi": "我们",    "pinyin": "wǒmen",      "meaning": "we; us"},
    {"hanzi": "五",      "pinyin": "wǔ",         "meaning": "five"},
    {"hanzi": "喜欢",    "pinyin": "xǐhuan",     "meaning": "to like"},
    {"hanzi": "下",      "pinyin": "xià",        "meaning": "down"},
    {"hanzi": "下午",    "pinyin": "xiàwǔ",      "meaning": "afternoon"},
    {"hanzi": "下雨",    "pinyin": "xiàyǔ",      "meaning": "to rain"},
    {"hanzi": "先生",    "pinyin": "xiānsheng",  "meaning": "Mr.; sir"},
    {"hanzi": "现在",    "pinyin": "xiànzài",    "meaning": "now"},
    {"hanzi": "想",      "pinyin": "xiǎng",      "meaning": "to want; to think"},
    {"hanzi": "小",      "pinyin": "xiǎo",       "meaning": "small"},
    {"hanzi": "小姐",    "pinyin": "xiǎojie",    "meaning": "Miss"},
    {"hanzi": "些",      "pinyin": "xiē",        "meaning": "some"},
    {"hanzi": "写",      "pinyin": "xiě",        "meaning": "to write"},
    {"hanzi": "谢谢",    "pinyin": "xièxie",     "meaning": "thank you"},
    {"hanzi": "星期",    "pinyin": "xīngqī",     "meaning": "week"},
    {"hanzi": "学生",    "pinyin": "xuésheng",   "meaning": "student"},
    {"hanzi": "学习",    "pinyin": "xuéxí",      "meaning": "to study"},
    {"hanzi": "学校",    "pinyin": "xuéxiào",    "meaning": "school"},
    {"hanzi": "一",      "pinyin": "yī",         "meaning": "one"},
    {"hanzi": "一点儿",  "pinyin": "yìdiǎnr",    "meaning": "a little"},
    {"hanzi": "衣服",    "pinyin": "yīfu",       "meaning": "clothes"},
    {"hanzi": "医生",    "pinyin": "yīshēng",    "meaning": "doctor"},
    {"hanzi": "医院",    "pinyin": "yīyuàn",     "meaning": "hospital"},
    {"hanzi": "椅子",    "pinyin": "yǐzi",       "meaning": "chair"},
    {"hanzi": "有",      "pinyin": "yǒu",        "meaning": "to have"},
    {"hanzi": "月",      "pinyin": "yuè",        "meaning": "month"},
    {"hanzi": "再见",    "pinyin": "zàijiàn",    "meaning": "goodbye"},
    {"hanzi": "在",      "pinyin": "zài",        "meaning": "at; in; on"},
    {"hanzi": "怎么",    "pinyin": "zěnme",      "meaning": "how"},
    {"hanzi": "怎么样",  "pinyin": "zěnmeyàng", "meaning": "how about"},
    {"hanzi": "这",      "pinyin": "zhè",        "meaning": "this"},
    {"hanzi": "这儿",    "pinyin": "zhèr",       "meaning": "here"},
    {"hanzi": "中国",    "pinyin": "Zhōngguó",   "meaning": "China"},
    {"hanzi": "中午",    "pinyin": "zhōngwǔ",    "meaning": "noon"},
    {"hanzi": "住",      "pinyin": "zhù",        "meaning": "to live"},
    {"hanzi": "桌子",    "pinyin": "zhuōzi",     "meaning": "table"},
    {"hanzi": "字",      "pinyin": "zì",         "meaning": "character"}
]

def seed_hsk1():
    """Seeds the database with all 150 HSK 1 words."""
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Insert each HSK 1 entry
        for entry in HSK1_WORDS:
            char = Character(
                hanzi=entry["hanzi"],
                pinyin=entry["pinyin"],
                meaning=entry["meaning"],
                stroke_count=0,  # Or set actual stroke counts if you wish
                difficulty=1,
                radical=None,
                etymology="HSK1",
                mnemonic=""
            )
            db.session.add(char)

        db.session.commit()
        print("Successfully inserted all 150 HSK 1 words!")

if __name__ == "__main__":
    seed_hsk1()