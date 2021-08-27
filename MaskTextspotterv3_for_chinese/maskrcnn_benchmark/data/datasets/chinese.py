# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
"""
Simple dataset class that wraps a list of path names
"""

import os

import numpy as np
import torch
from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.structures.segmentation_mask import (
    SegmentationCharMask,
    SegmentationMask,
)
from PIL import Image, ImageDraw


class ChineseDataset(object):
    def __init__(self, use_charann, imgs_dir, gts_dir, transforms=None, ignore_difficult=False):
        self.use_charann = use_charann
        self.image_lists = [os.path.join(imgs_dir, img) for img in os.listdir(imgs_dir)]
        # print(imgs_dir)
        self.gts_dir = gts_dir
        self.transforms = transforms
        self.min_proposal_size = 2
        self.char_classes = "_0123456789abcdefghijklmnopqrstuvwxyz一丁七万丈三上下不与丐丑专且世丘业丛东丝丞丢两严丧个丫中丰串临丸丹为主丽举乃久么义之乌乍乎乏乐乒乓乔乖乘乙九乞也习乡书买乱乳乾了予争事二于亏云互五井亚些亡亢交亦产亨享京亭亮亲人亿什仁仅仆仇今介仍从仑仓仔仕他仗付仙仝代令以仪们仰仲件价任份仿企伊伍伏伐休众优伙会伞伟传伢伤伦伪伯估伴伶伸伺似伽但位低住佐佑体何佘余佚佛作佟你佣佩佬佰佳使侃侄侈例侍侏供依侠侣侥侦侧侨侬侮侯侵便促俄俊俏俐俑俗俘俚保信俩俪俭修俯俱倍倒倔候倚借倩债值倾假偏做停健偶偷偿傀傅储催傲傻像僚僧僵僻儡儿允元兄充兆先光克免兑兔党兜入全八公六兮兰共关兴兵其具典兹养兼兽内冈册再冒冕写军农冠冢冤冥冬冯冰冲决况冷冻净凄准凉凋凌减凑凛凝几凡凤凭凯凳凶凹出击函刀刁刃分切刊刑划列刘则刚创初删判刨利别刮到制刷券刹刺刻剁剂剃削前剑剔剖剥剧剩剪副割剿劈力劝办功加务劣动助努劫励劲劳劾势勃勇勉勋勒募勤勺勾勿匀包匆匈匕化北匙匠匡匣匪匮匹区医匿十千升午半华协卑卒卓单卖南博卜占卡卢卤卧卫卯印危即却卵卷卸卿厂厄厅历厉压厌厕厘厚原厢厥厦厨厮去县参又叉及友双反发叔取受变叙叛叠口古句另叨叩只叫召叭叮可台叱史右叶号司叹吁吃各合吉吊同名后吐向吓吕吗君吞吟否吧吨含听吭吮启吴吵吸吹吻吼吾呀呆呈告呐呕呗员呛呜周呱味呵呼命咆咋和咏咒咔咕咖咙咚咧咪咬咱咳咸咽哀品哄哇哈哉响哎哑哥哧哨哩哪哭哮哲哺哼哽唇唏唐唠唢唤唧唬售唯唱唾商啊啕啡啤啥啦啸喀喂善喇喉喊喘喜喝喧喱喷喻嗑嗓嗜嗷嗽嘀嘉嘎嘘嘛嘟嘣嘲嘴嘶嘹嘻嘿噗噜器噩噪噬噱嚎嚏嚣嚼囊囚四回因团囤园困围固国图圆圈土圣在圭地圳场圻圾址坂均坊坍坎坏坐坑块坚坛坞坟坠坡坤坦坷垂垃垄型垒垠垫垮埃埋城埔域培基堂堆堑堕堡堪堵塌塑塔塘塞填境墅墓墙增墟墨壁壕士壮声壳壶壹处备复夏夕外多夜够大天太夫央失头夷夸夹夺奂奇奈奉奋奎奏契奔奕奖套奠奢奥女奴奶奸她好如妃妄妆妇妈妍妒妓妖妙妞妥妨妩妮妹妻姆姊始姐姑姓委姗姚姜姥姨姬姻姿威娃娄娅娆娇娑娓娘娜娟娥娩娱娲娴娶婆婉婕婚婧婪婴婶婷婿媒媚媛媲媳嫁嫂嫉嫌嫖嫣嫦嫩子孔孕字存孙孜孝孟孢季孤学孩孰孵孽宁它宅宇守安宋完宏宕宗官宙定宛宜宝实宠审客宣室宥宪宫宰害宴宵家容宽宾宿寂寄寅密寇富寐寒寓寞察寡寨寰寸对寺寻导寿封射将尉尊小少尔尖尘尚尝尤尬就尴尸尹尺尼尽尾尿局屁层居屈届屋屎屏展属屠屡履屯山屿岁岂岌岐岔岗岚岛岩岭岳岸岿峙峡峥峰峻崇崎崔崖崛崩崭崽嵌嵘嵩巅巍川州巡巢工左巧巨巩巫差己已巳巴巷巾币市布帅帆师希帐帕帖帘帝带帧席帮常帽幂幅幕干平年并幸幻幼幽广庄庆床序库应底店庙庚府庞废度座庭庵康庸廉廊廖延廷建开异弃弄弈弊式弑弓引弗弘弟张弥弦弧弩弯弱弹强归当录彗形彤彦彩彪彬彭彰影彷役彻彼往征径待很律徐徒得徙御徨循微德徽心必忆忌忍忏忐忑志忘忙忠忧快念忽怀态怂怎怒怔怕怖怜思怡急怦性怨怪总怼恋恍恐恒恕恙恢恨恩恬恭息恰恳恶恼悄悉悍悔悖悟悠患悦悬悲悴悸悼情惊惋惑惕惜惠惧惨惩惫惬惭惮惯惰想惹愁愈愉意愚感愣愤愧愿慈慌慎慑慕慢慧慨慰慵憋憎憔憨憾懂懈懒懦懵懿戈戏成我戒或战戚戟截戬戮戳戴户房所扁扇扉手才扎扑扒打扔托扛扣执扩扫扬扭扮扯扰扳扶批扼找承技抄抉把抑抒抓投抖抗折抚抛抠抢护报抨披抬抱抵抹押抽拂担拆拇拉拌拍拐拒拓拔拖拗招拜拟拢拥拦拨择括拭拯拳拷拼拾拿持挂指按挑挖挚挞挡挣挤挥挨挪挫振挺挽捂捆捉捋捍捏捐捕捞损捡换捣捧据捷掀授掉掌掏排掘掠探接控推掩措掰掳掷揍描提插握揪揭援揽搁搅搏搓搜搞搪搬搭携摄摆摇摊摔摘摧摩摸摹撂撑撒撕撞撤撩播撮撼擂擅操擎擒擦攀攒支收改攻放政故效敌敏救教敛敞敢散敦敬数敲整敷文斋斌斐斑斓斗料斜斤斥斧斩断斯新方施旁旅旋族旗无既日旦旧早旬旭旱时旷旺昂昆昊昌明昏易昔昕昙星映春昧昨昭是昵昼显晃晋晒晓晕晗晚晨普景晰晴晶智暂暇暑暖暗暧暮暴曙曜曝曰曲曳更曹曼曾替最月有朋服朔朗望朝期木未末本术朱朴朵机朽杀杂权杆杉李杏材村杖杜杞束杠条来杨杭杯杰杷松板极构枇枉析枕林枚果枝枪枫枭枯架枸柄柏某柒染柔柚柜柠查柬柯柱柳柴柿标栈栋栎栏树栓栗校株样核根格栽桀桂桃框案桌桐桑档桥桨桩桶梁梅梓梗梦梧梨梭梯械梳梵检棉棋棍棒棕棘棚棠森棱棵棺椅植椎椒椭椰楚楠楼概榄榆榜榨榫榴槌槛槟槽樊模横樱樽樾橄橘橙橡橱檀檐檬欠次欢欣欧欲欺款歇歉歌止正此步武歧歪歹死歼殃殆殇殊残殖殡殴段殿毁毅毋母每毒比毕毙毛毡毫氏民氓气氛氢氦氧氮氯水永汀汁求汇汉汐汕汗江池污汤汪汰汹汽沃沈沉沌沐沙沛沟没沦沧沪沫河沸油治沼沿泄泉泊泓法泛泡波泣泥注泪泫泯泰泳泵泼泽洁洋洒洗洙洛洞津洪洱洲活洽派流浅浆浇测济浏浑浒浓浙浚浣浦浩浪浮浴海浸涂涅消涉涌涎涛涡涤润涨涩涯液涵淀淆淇淋淌淑淘淡淬深混淹添清渊渐渔渗渡渣渤温港渲渴游渺湃湄湖湘湛湫湮湾湿溃溅源溜溢溪溶溺滁滋滑滔滚滞满滤滥滨滩滴漂漆漏漓演漠漩漫潇潘潜潦潮潸澄澈澎澜澡澳激濑濒濮瀑瀚瀛灌火灭灯灰灵灶灼灾灿炅炉炊炎炒炖炙炜炫炬炭炮炸点炼炽烂烈烘烙烛烟烤烦烧烨烩烫烬热烹烽焉焊焕焘焙焦焰然煌煎煜煞煤煦照煮煲煽熄熊熏熔熙熟熬燃燕燥爆爪爬爱爵父爷爸爹爽片版牌牙牛牡牢牧物牲牵特牺犀犄犬犯状犹狂狄狈狐狒狗狙狞狠狡狩独狭狮狰狱狸狼猁猎猕猖猛猜猝猞猥猩猪猫猬献猴猾獗獠獭玄率玉王玑玖玛玩玫玮环现玲玳玺玻珀珉珊珍珑珠班球理琉琏琐琢琥琦琪琳琴琵琶琼瑁瑕瑚瑜瑞瑟瑰瑶瑾璀璃璇璨瓜瓢瓣瓦瓶瓷甄甘甚甜生用甩甫田由甲申电男甸画畅界畏畔留畜略番畸疆疏疑疗疙疡疤疫疯疲疵疼疾病症痒痕痘痛痞痣痧痪痴瘟瘤瘦瘩瘫瘸瘾癌癖癞癫登白百皂的皆皇皓皙皮皱盆盈益盐监盒盔盖盗盘盛盟目盯盲直相盼盾省眉看真眠眨眩眶眷眸眼着睁睐睑睛睡督睦睹睽睿瞄瞎瞑瞒瞠瞧瞪瞬瞰瞳瞻矛矜矢知矩矫短矮石矶矿码砂砍砒研砖砥破砸础硅硕硬确碉碌碍碎碑碗碟碧碰碳碴碾磁磅磊磋磕磨磷礴示礼社祁祈祖祛祝神祟祥票祭祷祸祺禀禁禄禅福禹禺离禽秀私秃秋种科秒秘租秤秦秧秩积称移秽稀程稍税稚稠稣稳稻稼稽稿穆穗穴究穷穹空穿突窃窄窍窒窗窝窟窥窿立竖站竞竟章竣童竭端竹竿笋笑笔笙笛笠符笨第笼等筋筏筐筑筒答策筛筝筠筷筹签简箍算管箭箱篇篡篮篷簿籁籍米类粉粒粗粘粤粥粪粮粱粹粽精糊糕糖糙糟糯系素索紧紫累絮繁纠红纤约级纪纫纬纭纯纱纲纳纵纷纸纹纽线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绣继绩绪绫续绮绯绳维绵绷综绽绿缅缆缉缎缓缔编缘缚缜缝缠缩缭缰缴缸缺罄罐网罕罗罚罢罩罪置羁羊美羔羞羡群羲羹羽羿翁翅翔翟翠翡翩翰翱翻翼耀老考者而耍耐耕耗耳耶耸耻耽耿聂聆聊聋职联聘聚聪肃肆肇肉肋肌肖肘肚肝肠股肢肤肥肩肪肮肯育肺肾肿胀胁胃胆背胎胖胚胛胜胞胡胭胯胳胶胸能脂脆脉脊脏脐脑脓脖脚脱脸脾腆腊腌腐腔腕腥腩腮腰腱腹腺腻腼腾腿膀膊膏膑膛膜膝膨膳膺臀臂臣自臭至致臼舅舆舌舍舒舜舞舟航般舰舱船艇艘良艰色艳艺艾节芋芒芙芜芝芦芬芭芯花芳芽苇苍苏苑苔苗苛苟若苦英苹茂范茄茅茉茜茧茨茫茬茵茶茸茹荃荆草荐荒荔荞荡荣荤荧药荷莉莎莓莞莫莱莲获莹莺莽菇菊菌菜菠菩菱菲萃萄萌萍萝萤营萧萨萱落著葛葡董葩葫葬葱葳葵蒂蒋蒙蒜蒲蒸蓄蓉蓓蓝蓬蔑蔓蔗蔚蔡蔬蔷蔻蕉蕙蕴蕾薄薇薛薪薯薰藉藏藕藤蘑虎虏虐虑虚虞虫虹虽虾蚀蚁蚂蚊蚓蚝蚣蚪蚯蛇蛊蛋蛔蛙蛛蛟蛤蛭蛮蛰蛳蛾蜂蜃蜈蜊蜓蜕蜗蜘蜜蜡蜢蜥蜴蜻蝇蝈蝉蝌蝎蝙蝠蝴蝶螂螃融螨螳螺蟆蟑蟒蟹蠕蠢血衅行衍衔街衡衣补表衫衬衰衷袁袋袍袖袜被袭袱裁裂装裔裕裙裤裳裴裸裹褒褪褶西要覆见观规觅视览觉觑角解触言詹誉誓警计订认讧讨让讪训议讯记讲讶许论讽设访诀证诃评诅识诈诉诊词译试诗诚诛话诞诟诠诡询该详诧诫诬语误诱说诵请诸诺读课谁调谄谅谈谊谋谍谎谐谓谔谕谚谛谜谢谣谦谨谩谪谬谭谱谴谷豆豉豌豚象豪豫豹貂貌贝贞负贡财责贤败账货质贩贪贫贬购贯贱贴贵贷贸费贺贼贾赃资赋赌赎赏赐赓赔赖赘赚赛赞赠赡赢赣赤赫走赴赵赶起趁超越趟趣足趴趾跃跋跌跑跛距跟跤跨跪路跳跷跺踏踝踢踩踪蹂蹄蹈蹊蹋蹑蹦蹬蹶蹼蹿躁躏身躬躯躲躺车轨轩转轮软轰轲轴轶轻载轿较辅辆辈辉辍辐辑输辕辗辙辛辜辞辟辣辨辩辰辱边辽达迁迄迅过迈迎运近返还这进远违连迟迢迦迪迫迭述迷迹追退送适逃逅逆选逊逍透逐递途逗通逛逝逞速造逢逮逸逻逼遁遂遇遍遏道遗遛遢遣遥遨遭遮遵避邀邂邋邓那邦邪邮邱邻郁郅郊郎郑郜郝部郭都鄙酉酋配酒酗酣酥酪酬酱酷酸酿醉醋醒醛醺采释里重野量金釜鉴鑫针钉钓钞钟钢钥钦钧钩钮钰钱钵钻铁铂铃铅铛铜铝铠铤铭铮铲银铸铺链铿销锁锅锈锋锏锐锒错锡锢锤锥锦键锯锵锻镀镁镇镑镓镖镜镭镯镰长门闪闭问闯闲间闷闸闹闺闻闽阀阁阅阈阉阎阑阔队阮阱防阳阴阵阶阻阿陀附际陆陈陋陌降限陕陛院除陨险陪陵陶陷隆隋随隐隔障隧隶隽难雀雁雄雅集雇雉雌雏雕雨雪雯雳零雷雾需霄霆震霉霍霏霓霖霜霞霰露霸霹青靓靖静非靠靡面革靴靶鞋鞘鞠鞭韦韧韩韭音韵韶页顶顷项顺须顽顾顿颁颂预颅领颇颈频颓颖颗题颚颜额颠颤风飒飓飘飙飞食餐饥饨饪饭饮饰饱饲饴饶饺饼饿馄馆馈馋馍馒首馗香馥馨马驭驯驰驱驴驶驹驻驼驾驿骁骂骄骆骇骋验骏骐骑骗骚骡骤骨骰骷骸骼髅髓高髦鬟鬼魁魂魄魅魇魈魏魔鱼鱿鲁鲈鲍鲜鲤鲨鲮鲱鲷鲸鳄鳅鳗鸟鸡鸢鸣鸦鸭鸯鸳鸽鸿鹃鹅鹈鹉鹊鹌鹏鹑鹕鹤鹦鹫鹰鹿麋麒麟麦麻麾黄黎黏黑默黛黯鼎鼓鼠鼹鼻鼾齐齿龄龙龟"
        # self.char_classes = "_0123456789abcdefghijklmnopqrstuvwxyz一丁七万丈三上下不与丐丑专且世丘业丛东丝丞丢两严丧个丫中丰串临丸丹为主丽举乃久么义之乌乍乎乏乐乒乓乔乖乘乙九乞也习乡书买乱乳乾了予争事二于亏云互五井亚些亡亢交亦产亨享京亭亮亲人亿什仁仅仆仇今介仍从仑仓仔仕他仗付仙仝代令以仪们仰仲件价任份仿企伊伍伏伐休众优伙会伞伟传伢伤伦伪伯估伴伶伸伺似伽但位低住佐佑体何佘余佚佛作佟你佣佩佬佰佳使侃侄侈例侍侏供依侠侣侥侦侧侨侬侮侯侵便促俄俊俏俐俑俗俘俚保信俩俪俭修俯俱倍倒倔候倚借倩债值倾假偏做停健偶偷偿傀傅储催傲傻像僚僧僵僻儡儿允元兄充兆先光克免兑兔党兜入全八公六兮兰共关兴兵其具典兹养兼兽内冈册再冒冕写军农冠冢冤冥冬冯冰冲决况冷冻净凄准凉凋凌减凑凛凝几凡凤凭凯凳凶凹出击函刀刁刃分切刊刑划列刘则刚创初删判刨利别刮到制刷券刹刺刻剁剂剃削前剑剔剖剥剧剩剪副割剿劈力劝办功加务劣动助努劫励劲劳劾势勃勇勉勋勒募勤勺勾勿匀包匆匈匕化北匙匠匡匣匪匮匹区医匿十千升午半华协卑卒卓单卖南博卜占卡卢卤卧卫卯印危即却卵卷卸卿厂厄厅历厉压厌厕厘厚原厢厥厦厨厮去县参又叉及友双反发叔取受变叙叛叠口古句另叨叩只叫召叭叮可台叱史右叶号司叹吁吃各合吉吊同名后吐向吓吕吗君吞吟否吧吨含听吭吮启吴吵吸吹吻吼吾呀呆呈告呐呕呗员呛呜周呱味呵呼命咆咋和咏咒咔咕咖咙咚咧咪咬咱咳咸咽哀品哄哇哈哉响哎哑哥哧哨哩哪哭哮哲哺哼哽唇唏唐唠唢唤唧唬售唯唱唾商啊啕啡啤啥啦啸喀喂善喇喉喊喘喜喝喧喱喷喻嗑嗓嗜嗷嗽嘀嘉嘎嘘嘛嘟嘣嘲嘴嘶嘹嘻嘿噗噜器噩噪噬噱嚎嚏嚣嚼囊囚四回因团囤园困围固国图圆圈土圣在圭地圳场圻圾址坂均坊坍坎坏坐坑块坚坛坞坟坠坡坤坦坷垂垃垄型垒垠垫垮埃埋城埔域培基堂堆堑堕堡堪堵塌塑塔塘塞填境墅墓墙增墟墨壁壕士壮声壳壶壹处备复夏夕外多夜够大天太夫央失头夷夸夹夺奂奇奈奉奋奎奏契奔奕奖套奠奢奥女奴奶奸她好如妃妄妆妇妈妍妒妓妖妙妞妥妨妩妮妹妻姆姊始姐姑姓委姗姚姜姥姨姬姻姿威娃娄娅娆娇娑娓娘娜娟娥娩娱娲娴娶婆婉婕婚婧婪婴婶婷婿媒媚媛媲媳嫁嫂嫉嫌嫖嫣嫦嫩子孔孕字存孙孜孝孟孢季孤学孩孰孵孽宁它宅宇守安宋完宏宕宗官宙定宛宜宝实宠审客宣室宥宪宫宰害宴宵家容宽宾宿寂寄寅密寇富寐寒寓寞察寡寨寰寸对寺寻导寿封射将尉尊小少尔尖尘尚尝尤尬就尴尸尹尺尼尽尾尿局屁层居屈届屋屎屏展属屠屡履屯山屿岁岂岌岐岔岗岚岛岩岭岳岸岿峙峡峥峰峻崇崎崔崖崛崩崭崽嵌嵘嵩巅巍川州巡巢工左巧巨巩巫差己已巳巴巷巾币市布帅帆师希帐帕帖帘帝带帧席帮常帽幂幅幕干平年并幸幻幼幽广庄庆床序库应底店庙庚府庞废度座庭庵康庸廉廊廖延廷建开异弃弄弈弊式弑弓引弗弘弟张弥弦弧弩弯弱弹强归当录彗形彤彦彩彪彬彭彰影彷役彻彼往征径待很律徐徒得徙御徨循微德徽心必忆忌忍忏忐忑志忘忙忠忧快念忽怀态怂怎怒怔怕怖怜思怡急怦性怨怪总怼恋恍恐恒恕恙恢恨恩恬恭息恰恳恶恼悄悉悍悔悖悟悠患悦悬悲悴悸悼情惊惋惑惕惜惠惧惨惩惫惬惭惮惯惰想惹愁愈愉意愚感愣愤愧愿慈慌慎慑慕慢慧慨慰慵憋憎憔憨憾懂懈懒懦懵懿戈戏成我戒或战戚戟截戬戮戳戴户房所扁扇扉手才扎扑扒打扔托扛扣执扩扫扬扭扮扯扰扳扶批扼找承技抄抉把抑抒抓投抖抗折抚抛抠抢护报抨披抬抱抵抹押抽拂担拆拇拉拌拍拐拒拓拔拖拗招拜拟拢拥拦拨择括拭拯拳拷拼拾拿持挂指按挑挖挚挞挡挣挤挥挨挪挫振挺挽捂捆捉捋捍捏捐捕捞损捡换捣捧据捷掀授掉掌掏排掘掠探接控推掩措掰掳掷揍描提插握揪揭援揽搁搅搏搓搜搞搪搬搭携摄摆摇摊摔摘摧摩摸摹撂撑撒撕撞撤撩播撮撼擂擅操擎擒擦攀攒支收改攻放政故效敌敏救教敛敞敢散敦敬数敲整敷文斋斌斐斑斓斗料斜斤斥斧斩断斯新方施旁旅旋族旗无既日旦旧早旬旭旱时旷旺昂昆昊昌明昏易昔昕昙星映春昧昨昭是昵昼显晃晋晒晓晕晗晚晨普景晰晴晶智暂暇暑暖暗暧暮暴曙曜曝曰曲曳更曹曼曾替最月有朋服朔朗望朝期木未末本术朱朴朵机朽杀杂权杆杉李杏材村杖杜杞束杠条来杨杭杯杰杷松板极构枇枉析枕林枚果枝枪枫枭枯架枸柄柏某柒染柔柚柜柠查柬柯柱柳柴柿标栈栋栎栏树栓栗校株样核根格栽桀桂桃框案桌桐桑档桥桨桩桶梁梅梓梗梦梧梨梭梯械梳梵检棉棋棍棒棕棘棚棠森棱棵棺椅植椎椒椭椰楚楠楼概榄榆榜榨榫榴槌槛槟槽樊模横樱樽樾橄橘橙橡橱檀檐檬欠次欢欣欧欲欺款歇歉歌止正此步武歧歪歹死歼殃殆殇殊残殖殡殴段殿毁毅毋母每毒比毕毙毛毡毫氏民氓气氛氢氦氧氮氯水永汀汁求汇汉汐汕汗江池污汤汪汰汹汽沃沈沉沌沐沙沛沟没沦沧沪沫河沸油治沼沿泄泉泊泓法泛泡波泣泥注泪泫泯泰泳泵泼泽洁洋洒洗洙洛洞津洪洱洲活洽派流浅浆浇测济浏浑浒浓浙浚浣浦浩浪浮浴海浸涂涅消涉涌涎涛涡涤润涨涩涯液涵淀淆淇淋淌淑淘淡淬深混淹添清渊渐渔渗渡渣渤温港渲渴游渺湃湄湖湘湛湫湮湾湿溃溅源溜溢溪溶溺滁滋滑滔滚滞满滤滥滨滩滴漂漆漏漓演漠漩漫潇潘潜潦潮潸澄澈澎澜澡澳激濑濒濮瀑瀚瀛灌火灭灯灰灵灶灼灾灿炅炉炊炎炒炖炙炜炫炬炭炮炸点炼炽烂烈烘烙烛烟烤烦烧烨烩烫烬热烹烽焉焊焕焘焙焦焰然煌煎煜煞煤煦照煮煲煽熄熊熏熔熙熟熬燃燕燥爆爪爬爱爵父爷爸爹爽片版牌牙牛牡牢牧物牲牵特牺犀犄犬犯状犹狂狄狈狐狒狗狙狞狠狡狩独狭狮狰狱狸狼猁猎猕猖猛猜猝猞猥猩猪猫猬献猴猾獗獠獭玄率玉王玑玖玛玩玫玮环现玲玳玺玻珀珉珊珍珑珠班球理琉琏琐琢琥琦琪琳琴琵琶琼瑁瑕瑚瑜瑞瑟瑰瑶瑾璀璃璇璨瓜瓢瓣瓦瓶瓷甄甘甚甜生用甩甫田由甲申电男甸画畅界畏畔留畜略番畸疆疏疑疗疙疡疤疫疯疲疵疼疾病症痒痕痘痛痞痣痧痪痴瘟瘤瘦瘩瘫瘸瘾癌癖癞癫登白百皂的皆皇皓皙皮皱盆盈益盐监盒盔盖盗盘盛盟目盯盲直相盼盾省眉看真眠眨眩眶眷眸眼着睁睐睑睛睡督睦睹睽睿瞄瞎瞑瞒瞠瞧瞪瞬瞰瞳瞻矛矜矢知矩矫短矮石矶矿码砂砍砒研砖砥破砸础硅硕硬确碉碌碍碎碑碗碟碧碰碳碴碾磁磅磊磋磕磨磷礴示礼社祁祈祖祛祝神祟祥票祭祷祸祺禀禁禄禅福禹禺离禽秀私秃秋种科秒秘租秤秦秧秩积称移秽稀程稍税稚稠稣稳稻稼稽稿穆穗穴究穷穹空穿突窃窄窍窒窗窝窟窥窿立竖站竞竟章竣童竭端竹竿笋笑笔笙笛笠符笨第笼等筋筏筐筑筒答策筛筝筠筷筹签简箍算管箭箱篇篡篮篷簿籁籍米类粉粒粗粘粤粥粪粮粱粹粽精糊糕糖糙糟糯系素索紧紫累絮繁纠红纤约级纪纫纬纭纯纱纲纳纵纷纸纹纽线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绣继绩绪绫续绮绯绳维绵绷综绽绿缅缆缉缎缓缔编缘缚缜缝缠缩缭缰缴缸缺罄罐网罕罗罚罢罩罪置羁羊美羔羞羡群羲羹羽羿翁翅翔翟翠翡翩翰翱翻翼耀老考者而耍耐耕耗耳耶耸耻耽耿聂聆聊聋职联聘聚聪肃肆肇肉肋肌肖肘肚肝肠股肢肤肥肩肪肮肯育肺肾肿胀胁胃胆背胎胖胚胛胜胞胡胭胯胳胶胸能脂脆脉脊脏脐脑脓脖脚脱脸脾腆腊腌腐腔腕腥腩腮腰腱腹腺腻腼腾腿膀膊膏膑膛膜膝膨膳膺臀臂臣自臭至致臼舅舆舌舍舒舜舞舟航般舰舱船艇艘良艰色艳艺艾节芋芒芙芜芝芦芬芭芯花芳芽苇苍苏苑苔苗苛苟若苦英苹茂范茄茅茉茜茧茨茫茬茵茶茸茹荃荆草荐荒荔荞荡荣荤荧药荷莉莎莓莞莫莱莲获莹莺莽菇菊菌菜菠菩菱菲萃萄萌萍萝萤营萧萨萱落著葛葡董葩葫葬葱葳葵蒂蒋蒙蒜蒲蒸蓄蓉蓓蓝蓬蔑蔓蔗蔚蔡蔬蔷蔻蕉蕙蕴蕾薄薇薛薪薯薰藉藏藕藤蘑虎虏虐虑虚虞虫虹虽虾蚀蚁蚂蚊蚓蚝蚣蚪蚯蛇蛊蛋蛔蛙蛛蛟蛤蛭蛮蛰蛳蛾蜂蜃蜈蜊蜓蜕蜗蜘蜜蜡蜢蜥蜴蜻蝇蝈蝉蝌蝎蝙蝠蝴蝶螂螃融螨螳螺蟆蟑蟒蟹蠕蠢血衅行衍衔街衡衣补表衫衬衰衷袁袋袍袖袜被袭袱裁裂装裔裕裙裤裳裴裸裹褒褪褶西要覆见观规觅视览觉觑角解触言詹誉誓警计订认讧讨让讪训议讯记讲讶许论讽设访诀证诃评诅识诈诉诊词译试诗诚诛话诞诟诠诡询该详诧诫诬语误诱说诵请诸诺读课谁调谄谅谈谊谋谍谎谐谓谔谕谚谛谜谢谣谦谨谩谪谬谭谱谴谷豆豉豌豚象豪豫豹貂貌贝贞负贡财责贤败账货质贩贪贫贬购贯贱贴贵贷贸费贺贼贾赃资赋赌赎赏赐赓赔赖赘赚赛赞赠赡赢赣赤赫走赴赵赶起趁超越趟趣足趴趾跃跋跌跑跛距跟跤跨跪路跳跷跺踏踝踢踩踪蹂蹄蹈蹊蹋蹑蹦蹬蹶蹼蹿躁躏身躬躯躲躺车轨轩转轮软轰轲轴轶轻载轿较辅辆辈辉辍辐辑输辕辗辙辛辜辞辟辣辨辩辰辱边辽达迁迄迅过迈迎运近返还这进远违连迟迢迦迪迫迭述迷迹追退送适逃逅逆选逊逍透逐递途逗通逛逝逞速造逢逮逸逻逼遁遂遇遍遏道遗遛遢遣遥遨遭遮遵避邀邂邋邓那邦邪邮邱邻郁郅郊郎郑郜郝部郭都鄙酉酋配酒酗酣酥酪酬酱酷酸酿醉醋醒醛醺采释里重野量金釜鉴鑫针钉钓钞钟钢钥钦钧钩钮钰钱钵钻铁铂铃铅铛铜铝铠铤铭铮铲银铸铺链铿销锁锅锈锋锏锐锒错锡锢锤锥锦键锯锵锻镀镁镇镑镓镖镜镭镯镰长门闪闭问闯闲间闷闸闹闺闻闽阀阁阅阈阉阎阑阔队阮阱防阳阴阵阶阻阿陀附际陆陈陋陌降限陕陛院除陨险陪陵陶陷隆隋随隐隔障隧隶隽难雀雁雄雅集雇雉雌雏雕雨雪雯雳零雷雾需霄霆震霉霍霏霓霖霜霞霰露霸霹青靓靖静非靠靡面革靴靶鞋鞘鞠鞭韦韧韩韭音韵韶页顶顷项顺须顽顾顿颁颂预颅领颇颈频颓颖颗题颚颜额颠颤风飒飓飘飙飞食餐饥饨饪饭饮饰饱饲饴饶饺饼饿馄馆馈馋馍馒首馗香馥馨马驭驯驰驱驴驶驹驻驼驾驿骁骂骄骆骇骋验骏骐骑骗骚骡骤骨骰骷骸骼髅髓高髦鬟鬼魁魂魄魅魇魈魏魔鱼鱿鲁鲈鲍鲜鲤鲨鲮鲱鲷鲸鳄鳅鳗鸟鸡鸢鸣鸦鸭鸯鸳鸽鸿鹃鹅鹈鹉鹊鹌鹏鹑鹕鹤鹦鹫鹰鹿麋麒麟麦麻麾黄黎黏黑默黛黯鼎鼓鼠鼹鼻鼾齐齿龄龙龟！？。()%\《》[]：#&+=；/—"
        # self.char_classes = "_0123456789abcdefghijklmnopqrstuvwxyz\#%&()+/=[]—。《》一丁七万丈三上下不与丐丑专且世丘业丛东丝丞丢两严丧个丫中丰串临丸丹为主丽举乃久么义之乌乍乎乏乐乒乓乔乖乘乙九乞也习乡书买乱乳乾了予争事二于亏云互五井亚些亡亢交亦产亨享京亭亮亲人亿什仁仅仆仇今介仍从仑仓仔仕他仗付仙仝代令以仪们仰仲件价任份仿企伊伍伎伏伐休众优伙会伞伟传伢伤伦伪伯估伴伶伸伺似伽但位低住佐佑体何佗佘余佚佛作佟你佣佩佬佰佳使侃侄侈例侍侏侗供依侠侣侥侦侧侨侬侮侯侵便促俄俊俏俐俑俗俘俚保俞信俩俪俭修俯俱倍倒倔候倚借倦倩倪债值倾假偏做停健偶偷偿傀傅傣储催傲傻像僚僧僮僵僻儒儡儿允元兄充兆先光克免兑兔党兜入全八公六兮兰共关兴兵其具典兹养兼兽内冈册再冒冕写军农冠冢冤冥冬冯冰冲决况冷冻净凄准凉凋凌减凑凛凝几凡凤凭凯凰凳凶凹出击函刀刁刃分切刊刑划列刘则刚创初删判刨利别刮到制刷券刹刺刻剁剂剃削前剑剔剖剥剧剩剪副割剿劈力劝办功加务劣动助努劫励劲劳劾势勃勇勉勋勒募勤勺勾勿匀包匆匈匕化北匙匠匡匣匪匮匹区医匿十千升午半华协卑卒卓单卖南博卜占卡卢卤卧卫卯印危即却卵卷卸卿厂厄厅历厉压厌厕厘厚原厢厥厦厨厮去县参又叉及友双反发叔取受变叙叛叠口古句另叨叩只叫召叭叮可台叱史右叶号司叹叽吁吃各合吉吊同名后吐向吒吓吕吗君吞吟否吧吨含听吭吮启吴吵吸吹吻吼吾呀呆呈告呐呕呗员呛呜周呱味呵呼命咆咋和咎咏咒咔咕咖咙咚咧咪咬咱咳咸咽哀品哄哇哈哉响哎哑哔哥哧哨哩哪哭哮哲哺哼哽唇唏唐唠唢唤唧唬售唯唱唾商啊啕啡啤啥啦啪啸啼喀喂善喇喉喊喘喜喝喧喱喷喻嗑嗓嗜嗷嗽嘀嘉嘎嘘嘛嘟嘣嘲嘴嘶嘹嘻嘿噗噜器噩噪噬噱嚎嚏嚣嚼囊囚四回因团囤园困囱围固国图圆圈土圣在圭地圳场圻圾址坂均坊坍坎坏坐坑块坚坛坝坞坟坠坡坤坦坷垂垃垄型垒垠垫垮埃埋城埔域培基堂堆堑堕堡堪堵塌塑塔塘塞填境墅墓墙增墟墨壁壑壕壤士壮声壳壶壹处备复夏夕外夙多夜够大天太夫央失头夷夸夹夺奂奇奈奉奋奎奏契奔奕奖套奠奢奥女奴奶奸她好如妃妄妆妇妈妍妒妓妖妙妞妥妨妩妮妹妻姆姊始姐姑姓委姗姚姜姥姨姬姻姿威娃娄娅娆娇娑娓娘娜娟娥娩娱娲娴娶婆婉婕婚婧婪婴婶婷婿媒媚媛媲媳嫁嫂嫉嫌嫖嫣嫦嫩嬴子孔孕字存孙孜孝孟孢季孤学孩孪孰孵孽宁它宅宇守安宋完宏宕宗官宙定宛宜宝实宠审客宣室宥宪宫宰害宴宵家容宽宾宿寂寄寅密寇富寐寒寓寝寞察寡寨寰寸对寺寻导寿封射将尉尊小少尔尖尘尚尝尤尬就尴尸尹尺尼尽尾尿局屁层居屈届屋屎屏展属屠屡履屯山屿岁岂岌岐岑岔岗岚岛岩岭岳岸岿峙峡峥峰峻崇崎崔崖崛崩崭崽嵌嵘嵩巅巍川州巡巢工左巧巨巩巫差己已巳巴巷巾币市布帅帆师希帐帕帖帘帝带帧席帮常帽幂幅幕幡干平年并幸幻幼幽广庄庆床序庐库应底店庙庚府庞废度座庭庵康庸庾廉廊廖延廷建开异弃弄弈弊式弑弓引弗弘弛弟张弥弦弧弩弯弱弹强归当录彗彝形彤彦彩彪彬彭彰影彷役彻彼往征径待很律徐徒得徙御徨循微德徽心必忆忌忍忏忐忑志忘忙忠忧快念忽怀态怂怎怒怔怕怖怜思怡急怦性怨怪总怼恋恍恐恒恕恙恢恨恩恬恭息恰恳恶恺恼悄悉悍悔悖悟悠患悦悬悲悴悸悼情惊惋惑惕惚惜惟惠惧惨惩惫惬惭惮惯惰想惹愁愈愉意愚感愣愤愧愿慈慌慎慑慕慢慧慨慰慵憋憎憔憨憾懂懈懒懦懵懿戈戏成我戒或战戚戛戟截戬戮戳戴户房所扁扇扉手才扎扑扒打扔托扛扣执扩扫扬扭扮扯扰扳扶批扼找承技抄抉把抑抒抓投抖抗折抚抛抠抢护报抨披抬抱抵抹押抽拂担拆拇拉拌拍拐拒拓拔拖拗拙招拜拟拢拥拦拨择括拭拯拱拳拷拼拾拿持挂指按挎挑挖挚挞挡挣挤挥挨挪挫振挺挽捂捆捉捋捍捏捐捕捞损捡换捣捧据捷掀授掉掌掏排掘掠探接控推掩措掰掳掷揉揍描提插握揪揭援揽搁搅搏搓搜搞搪搬搭携摄摆摇摊摔摘摧摩摸摹撂撑撒撕撞撤撩播撮撰撼擂擅操擎擒擦攀攒支收改攻放政故效敌敏救教敛敞敢散敦敬数敲整敷文斋斌斐斑斓斗料斜斤斥斧斩断斯新方施旁旅旋族旗无既日旦旧早旬旭旱时旷旺昂昆昊昌明昏易昔昕昙星映春昧昨昭是昵昼显晁晃晋晒晓晕晖晗晚晨普景晰晴晶智暂暇暑暖暗暧暮暴曙曜曝曰曲曳更曹曼曾替最月有朋服朔朗望朝期木未末本术朱朴朵机朽杀杂权杆杉李杏材村杖杜杞束杠条来杨杭杯杰杷松板极构枇枉析枕林枚果枝枪枫枭枯架枸柄柏某柒染柔柚柜柠查柬柯柱柳柴柿标栈栋栎栏树栓栖栗校株样核根格栽桀桂桃框案桌桐桑桔档桥桨桩桶梁梅梓梗梦梧梨梭梯械梳梵检棉棋棍棒棕棘棚棠森棱棵棺椅植椎椒椭椰椿楚楠楷楼概榄榆榜榨榫榴槌槛槟槽樊模横樯樱樽樾橄橘橙橡橱橹檀檄檐檬欠次欢欣欧欲欺款歇歉歌止正此步武歧歪歹死歼殃殆殇殊残殖殡殴段殷殿毁毅毋母每毒比毕毙毛毡毫毯氏民氓气氛氢氦氧氮氯水永汀汁求汇汉汐汕汗江池污汤汪汰汹汽沁沃沈沉沌沐沙沛沟没沦沧沪沫河沸油治沼沿泄泉泊泓法泛泡波泣泥注泪泫泯泰泳泵泼泽洁洋洒洗洙洛洞津洪洱洲活洽派流浅浆浇测济浏浑浒浓浙浚浣浦浩浪浮浴海浸涂涅消涉涌涎涛涡涤润涨涩涯液涵淀淆淇淋淌淑淘淞淡淬深淳混淹添清渊渍渐渔渗渝渡渣渤温港渲渴游渺湃湄湖湘湛湫湮湾湿溃溅源溜溢溥溪溶溺滁滋滑滔滕滚滞满滤滥滨滩滴漂漆漏漓演漠漩漪漫漾潇潘潜潦潭潮潸澄澈澎澜澡澳激濑濒濮瀑瀚瀛灌灏火灭灯灰灵灶灼灾灿炅炉炊炎炒炖炙炜炫炬炭炮炳炸点炼炽烂烈烘烙烛烟烤烦烧烨烩烫烬热烹烽焉焊焕焘焙焦焰焱然煌煎煜煞煤煦照煮煲煽熄熊熏熔熙熟熬燃燕燥爆爪爬爱爵父爷爸爹爽片版牌牙牛牡牢牧物牲牵特牺犀犄犬犯状犹狂狄狈狐狒狗狙狞狠狡狩独狭狮狰狱狸狼猁猎猕猖猛猜猝猞猥猩猪猫猬献猴猾猿獗獠獭玄率玉王玑玖玛玩玫玮环现玲玳玺玻珀珂珉珊珍珏珑珞珠班球理琉琏琐琢琥琦琪琳琴琵琶琼瑁瑕瑚瑜瑞瑟瑰瑶瑾璀璃璇璎璐璨瓜瓢瓣瓦瓶瓷甄甘甚甜生甥用甩甫田由甲申电男甸画畅界畏畔留畜略番畸疆疏疑疗疙疡疤疫疮疯疲疵疼疾病症痒痔痕痘痛痞痣痤痧痪痴瘟瘤瘦瘩瘫瘸瘾癌癖癞癫登白百皂的皆皇皓皙皮皱盆盈益盏盐监盒盔盖盗盘盛盟目盯盲直相盼盾省眉看真眠眨眩眶眷眸眼着睁睐睑睛睡督睦睫睹睽睿瞄瞎瞑瞒瞠瞧瞪瞬瞰瞳瞻瞿矛矜矢知矩矫短矮石矶矿码砂砍砒研砖砥破砸础硅硕硫硬确碉碌碍碎碑碗碟碧碰碳碴碾磁磅磊磋磕磨磷礴示礼社祁祈祖祛祝神祟祥票祭祷祸祺禀禁禄禅福禹禺离禽禾秀私秃秋种科秒秘租秤秦秧秩积称移秽稀程稍税稚稠稣稳稻稼稽稿穆穗穴究穷穹空穿突窃窄窍窒窗窝窟窥窿立竖站竞竟章竣童竭端竹竿笈笋笑笔笙笛笠符笨第笼等筋筏筐筑筒答策筛筝筠筷筹签简箍算管箭箱篇篡篮篷簧簿籁籍米类粉粒粗粘粤粥粪粮粱粹粽精糊糕糖糙糟糯系素索紧紫累絮繁纠红纤约级纪纫纬纭纯纱纲纳纵纷纸纹纺纽线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绣继绩绪绫续绮绯绰绳维绵绷综绽绿缅缆缉缎缓缔编缘缚缜缝缠缩缭缰缴缸缺罄罐网罕罗罚罢罩罪置羁羊羌美羔羞羡群羲羹羽羿翁翅翔翟翠翡翩翰翱翻翼耀老考者而耍耐耕耗耳耶耸耻耽耿聂聆聊聋职联聘聚聪肃肆肇肉肋肌肖肘肚肝肠股肢肤肥肩肪肮肯育肺肾肿胀胁胃胆背胎胖胚胛胜胞胡胭胯胳胶胸能脂脆脉脊脏脐脑脓脖脚脱脸脾腆腊腌腐腔腕腥腩腮腰腱腹腺腻腼腾腿膀膊膏膑膛膜膝膨膳膺臀臂臣臧自臭至致臼舅舆舌舍舒舜舞舟航般舰舱船艇艘良艰色艳艺艾节芋芒芙芜芝芥芦芬芭芮芯花芳芷芽苇苍苏苑苔苗苛苟若苦英苹茂范茄茅茉茜茧茨茫茬茵茶茸茹荃荆草荐荒荔荞荡荣荤荧药荷莆莉莎莓莞莫莱莲获莹莺莽菇菊菌菜菠菩菱菲萃萄萌萍萝萤营萧萨萱落葆著葛葡董葩葫葬葱葳葵蒂蒋蒙蒜蒲蒸蓄蓉蓓蓝蓬蔑蔓蔗蔚蔡蔬蔷蔻蕉蕙蕴蕾薄薇薛薪薯薰藉藏藕藤蘑虎虏虐虑虚虞虫虹虽虾蚀蚁蚂蚊蚓蚝蚣蚪蚯蚱蛇蛊蛋蛔蛙蛛蛟蛤蛭蛮蛰蛳蛾蜂蜃蜈蜊蜓蜕蜗蜘蜜蜡蜢蜥蜴蜻蝇蝈蝉蝌蝎蝙蝠蝴蝶蝼螂螃融螨螳螺螽蟆蟑蟒蟹蠕蠢血衅行衍衔街衡衣补表衩衫衬衰衷袁袋袍袖袜被袭袱裁裂装裔裕裙裤裳裴裸裹褒褪褶西要覆见观规觅视览觉觑角解触言詹誉誓警计订认讧讨让讪训议讯记讲讶许论讽设访诀证诃评诅识诈诉诊词译试诗诚诛话诞诟诠诡询该详诧诫诬语误诱说诵请诸诺读课谁调谄谅谈谊谋谌谍谎谐谓谔谕谚谛谜谢谣谦谨谩谪谬谭谱谴谷豆豉豌豚象豪豫豹豺貂貌贝贞负贡财责贤败账货质贩贪贫贬购贯贱贴贵贷贸费贺贼贾赃资赋赌赎赏赐赓赔赖赘赚赛赞赠赡赢赣赤赫走赴赵赶起趁超越趟趣足趴趾跃跋跌跑跛距跟跤跨跪路跳跷跺踏踝踢踩踪蹂蹄蹈蹊蹋蹑蹦蹬蹶蹼蹿躁躏身躬躯躲躺车轨轩转轮软轰轲轴轶轻载轿较辅辆辈辉辍辐辑输辕辗辙辛辜辞辟辣辨辩辰辱边辽达迁迄迅过迈迎运近返还这进远违连迟迢迦迪迫迭述迷迹追退送适逃逅逆选逊逍透逐递途逗通逛逝逞速造逢逮逵逸逻逼遁遂遇遍遏道遗遛遢遣遥遨遭遮遵避邀邂邋邑邓邝那邦邪邮邱邵邻郁郅郊郎郑郜郝郡部郭都鄙酉酋配酒酗酣酥酪酬酱酷酸酿醉醋醒醛醺采释里重野量金釜鉴鑫针钉钓钛钞钟钢钥钦钧钩钮钰钱钵钻铁铂铃铅铉铛铜铝铠铤铭铮铲银铸铺链铿销锁锂锅锈锋锏锐锒错锡锢锤锥锦键锯锵锻镀镁镇镐镑镓镖镜镭镯镰长门闪闭问闯闲间闷闸闹闺闻闽阀阁阅阈阉阎阑阔队阮阱防阳阴阵阶阻阿陀附际陆陈陋陌降限陕陛院除陨险陪陵陶陷隆隋随隐隔隙障隧隶隽难雀雁雄雅集雇雉雌雍雏雕雨雪雯雳零雷雾需霄霆震霉霍霏霓霖霜霞霰露霸霹青靓靖静非靠靡面革靳靴靶鞋鞘鞠鞭韦韧韩韭音韵韶页顶顷项顺须顽顾顿颁颂预颅领颇颈频颓颖颗题颚颜额颠颤风飒飓飘飙飞食餐餮饕饥饨饪饭饮饰饱饲饴饶饺饼饿馄馆馈馋馍馒首馗香馥馨马驭驯驰驱驳驴驶驹驻驼驾驿骁骂骄骆骇骋验骏骐骑骗骚骜骞骡骤骧骨骰骷骸骼髅髋髓高髦鬓鬟鬼魁魂魄魅魇魈魉魍魏魔鱼鱿鲁鲈鲍鲜鲤鲨鲮鲱鲲鲷鲸鳄鳅鳗鳞鸟鸡鸢鸣鸥鸦鸭鸯鸳鸽鸿鹃鹅鹈鹉鹊鹌鹏鹑鹕鹤鹦鹫鹰鹿麋麒麟麦麻麾黄黎黏黑默黛黯鼎鼓鼠鼹鼻鼾齐齿龄龊龌龙龚龟！：；？"
        self.vis = False
        self.ignore_difficult = ignore_difficult
        if self.ignore_difficult and self.gts_dir is not None and 'train' in self.gts_dir:
            self.image_lists = self.filter_image_lists()

    def filter_image_lists(self):
        new_image_lists = []
        for img_path in self.image_lists:
            has_positive = False
            im_name = os.path.basename(img_path)
            gt_path = os.path.join(self.gts_dir, "gt_"+im_name + ".txt")
            
            if not os.path.isfile(gt_path):
                gt_path = os.path.join(
                    self.gts_dir,  im_name.split(".")[0] + ".txt"
                )
            lines = open(gt_path, 'r').readlines()
            # print(lines)
            # print(gt_path)

            for line in lines:
                charbbs = []
                strs, loc = self.line2boxes(line)
                word = strs[0]
                if word == "###":
                    continue
                else:
                    has_positive = True
            if has_positive:
                new_image_lists.append(img_path)   
        return new_image_lists

    def __getitem__(self, item):
        # print('chinesedataset??????????????????')
        im_name = os.path.basename(self.image_lists[item])
        # print(self.image_lists)
        img = Image.open(self.image_lists[item]).convert("RGB")
        width, height = img.size
        # print(len(self.char_classes))
        if self.gts_dir is not None:
            gt_path = os.path.join(self.gts_dir, im_name + ".txt")
            if not os.path.isfile(gt_path):
                gt_path = os.path.join(
                    self.gts_dir, im_name.split(".")[0] + ".txt"
                )
            # print(gt_path)
            # print('wwwwwwwwwww?')
            words, boxes, charsbbs, segmentations, labels = self.load_gt_from_txt(
                gt_path, height, width
            )
            # print(words)
            # print(boxes)
            # print(charsbbs)
            # print(segmentations)
            # print(labels)
            # print('-------------')
            target = BoxList(
                boxes[:, :4], img.size, mode="xyxy", use_char_ann=self.use_charann
            )
            if self.ignore_difficult:
                labels = torch.from_numpy(np.array(labels))
            else:
                labels = torch.ones(len(boxes))
            target.add_field("labels", labels)
            masks = SegmentationMask(segmentations, img.size)
            target.add_field("masks", masks)
            if words[0] == "":
                use_char_ann = False
            else:
                use_char_ann = True
            if not self.use_charann:
                use_char_ann = False
            char_masks = SegmentationCharMask(
                charsbbs, words=words, use_char_ann=use_char_ann, size=img.size, char_num_classes=len(self.char_classes)
            )
            target.add_field("char_masks", char_masks)
        else:
            target = None
        if self.transforms is not None:
            img, target = self.transforms(img, target)
        if self.vis:
            new_im = img.numpy().copy().transpose([1, 2, 0]) + [
                102.9801,
                115.9465,
                122.7717,
            ]
            new_im = Image.fromarray(new_im.astype(np.uint8)).convert("RGB")
            mask = target.extra_fields["masks"].polygons[0].convert("mask")
            mask = Image.fromarray((mask.numpy() * 255).astype(np.uint8)).convert("RGB")
            if self.use_charann:
                m, _ = (
                    target.extra_fields["char_masks"]
                    .chars_boxes[0]
                    .convert("char_mask")
                )
                color = self.creat_color_map(37, 255)
                color_map = color[m.numpy().astype(np.uint8)]
                char = Image.fromarray(color_map.astype(np.uint8)).convert("RGB")
                char = Image.blend(char, new_im, 0.5)
            else:
                char = new_im
            new = Image.blend(char, mask, 0.5)
            img_draw = ImageDraw.Draw(new)
            for box in target.bbox.numpy():
                box = list(box)
                box = box[:2] + [box[2], box[1]] + box[2:] + [box[0], box[3]] + box[:2]
                img_draw.line(box, fill=(255, 0, 0), width=2)
            new.save("./vis/char_" + im_name)
        return img, target, self.image_lists[item]

    def creat_color_map(self, n_class, width):
        splits = int(np.ceil(np.power((n_class * 1.0), 1.0 / 3)))
        maps = []
        for i in range(splits):
            r = int(i * width * 1.0 / (splits - 1))
            for j in range(splits):
                g = int(j * width * 1.0 / (splits - 1))
                for k in range(splits - 1):
                    b = int(k * width * 1.0 / (splits - 1))
                    maps.append([r, g, b])
        return np.array(maps)

    def __len__(self):
        return len(self.image_lists)

    def load_gt_from_txt(self, gt_path, height=None, width=None):
        words, boxes, charsboxes, segmentations, labels = [], [], [], [], []
        lines = open(gt_path).readlines()
        for line in lines:
            charbbs = []
            strs, loc = self.line2boxes(line)
            word = strs[0]
            if word == "###":
                if self.ignore_difficult:
                    rect = list(loc[0])
                    min_x = min(rect[::2]) - 1
                    min_y = min(rect[1::2]) - 1
                    max_x = max(rect[::2]) - 1
                    max_y = max(rect[1::2]) - 1
                    box = [min_x, min_y, max_x, max_y]
                    segmentations.append([loc[0, :]])
                    tindex = len(boxes)
                    boxes.append(box)
                    words.append(word)
                    labels.append(-1)
                    charbbs = np.zeros((10,), dtype=np.float32)
                    if loc.shape[0] > 1:
                        for i in range(1, loc.shape[0]):
                            charbb[9] = tindex
                            charbbs.append(charbb.copy())
                        charsboxes.append(charbbs)
                else:
                    continue
            else:
                rect = list(loc[0])
                min_x = min(rect[::2]) - 1
                min_y = min(rect[1::2]) - 1
                max_x = max(rect[::2]) - 1
                max_y = max(rect[1::2]) - 1
                box = [min_x, min_y, max_x, max_y]
                segmentations.append([loc[0, :]])
                tindex = len(boxes)
                boxes.append(box)
                words.append(word)
                labels.append(1)
                c_class = self.char2num(strs[1:])
                charbb = np.zeros((10,), dtype=np.float32)
                if loc.shape[0] > 1:
                    for i in range(1, loc.shape[0]):
                        charbb[:8] = loc[i, :]
                        # try:
                        charbb[8] = c_class[i - 1]
                        # except: 
                        #     print(strs)
                        #     print(c_class)
                        #     print(i-1)
                        #     print(c_class[i - 1])
                        #     print('!!!!!!!!')
                        charbb[9] = tindex
                        charbbs.append(charbb.copy())
                    charsboxes.append(charbbs)
        num_boxes = len(boxes)
        if len(boxes) > 0:
            keep_boxes = np.zeros((num_boxes, 5))
            keep_boxes[:, :4] = np.array(boxes)
            keep_boxes[:, 4] = range(
                num_boxes
            )
            # the 5th column is the box label,
            # same as the 10th column of all charsboxes which belong to the box
            if self.use_charann:
                return words, np.array(keep_boxes), charsboxes, segmentations, labels
            else:
                charbbs = np.zeros((10,), dtype=np.float32)
                if len(charsboxes) == 0:
                    for _ in range(len(words)):
                        charsboxes.append([charbbs])
                return words, np.array(keep_boxes), charsboxes, segmentations, labels
        else:
            words.append("")
            charbbs = np.zeros((10,), dtype=np.float32)
            return (
                words,
                np.zeros((1, 5), dtype=np.float32),
                [[charbbs]],
                [[np.zeros((8,), dtype=np.float32)]],
                [1]
            )

    def line2boxes(self, line):
        parts = line.strip().split(",")
        if "\xef\xbb\xbf" in parts[0]:
            parts[0] = parts[0][3:]
        if "\ufeff" in parts[0]:
            parts[0] = parts[0].replace("\ufeff", "")
        # print(line)
        # print(parts)
        # print(parts[::9])
        x1 = np.array([int(float(x)) for x in parts[::9]])
        y1 = np.array([int(float(x)) for x in parts[1::9]])
        x2 = np.array([int(float(x)) for x in parts[2::9]])
        y2 = np.array([int(float(x)) for x in parts[3::9]])
        x3 = np.array([int(float(x)) for x in parts[4::9]])
        y3 = np.array([int(float(x)) for x in parts[5::9]])
        x4 = np.array([int(float(x)) for x in parts[6::9]])
        y4 = np.array([int(float(x)) for x in parts[7::9]])
        strs = parts[8::9]
        loc = np.vstack((x1, y1, x2, y2, x3, y3, x4, y4)).transpose()
        return strs, loc

    def check_charbbs(self, charbbs):
        xmins = np.minimum.reduce(
            [charbbs[:, 0], charbbs[:, 2], charbbs[:, 4], charbbs[:, 6]]
        )
        xmaxs = np.maximum.reduce(
            [charbbs[:, 0], charbbs[:, 2], charbbs[:, 4], charbbs[:, 6]]
        )
        ymins = np.minimum.reduce(
            [charbbs[:, 1], charbbs[:, 3], charbbs[:, 5], charbbs[:, 7]]
        )
        ymaxs = np.maximum.reduce(
            [charbbs[:, 1], charbbs[:, 3], charbbs[:, 5], charbbs[:, 7]]
        )
        return np.logical_and(
            xmaxs - xmins > self.min_proposal_size,
            ymaxs - ymins > self.min_proposal_size,
        )

    def check_charbb(self, charbb):
        xmins = min(charbb[0], charbb[2], charbb[4], charbb[6])
        xmaxs = max(charbb[0], charbb[2], charbb[4], charbb[6])
        ymins = min(charbb[1], charbb[3], charbb[5], charbb[7])
        ymaxs = max(charbb[1], charbb[3], charbb[5], charbb[7])
        return (
            xmaxs - xmins > self.min_proposal_size
            and ymaxs - ymins > self.min_proposal_size
        )
    def char2num(self, chars):
        ## chars ['h', 'e', 'l', 'l', 'o']
        nums = []
        for c in chars:
            # print(c)
            c = c.lower()
            # try:
            nums.append(self.char_classes.index(c))
            # except:
            #     print(c)
        return nums

    def get_img_info(self, item):
        """
        Return the image dimensions for the image, without
        loading and pre-processing it
        """

        im_name = os.path.basename(self.image_lists[item])
        img = Image.open(self.image_lists[item])
        width, height = img.size
        img_info = {"im_name": im_name, "height": height, "width": width}
        return img_info