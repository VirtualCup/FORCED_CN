from UnityText import UnityText;
from StringHelper import StringHelper;
from UnityUIfont import UnityUIfont;
from UnityFont import UnityFont;
import os, shutil;
import csv;
import sys;

reload(sys);
sys.setdefaultencoding('utf-8');

def save_to_csv():
	utxt = UnityText("OriginalFile/unnamed asset-resources.assets-1242.dat");
	rows = utxt.get_txt().split("\n");
	f = open("localization.csv", "wb");
	csv_writer = csv.writer(f);
	for row in rows:
		if row.find("|") == -1:
			csv_writer.writerow([row, "", "", ""]);
		else:
			namespace = row.split("|")[0].strip();
			id = row.split("|")[1].split("=")[0].strip();
			lang = row.split("|")[1].split("=")[1].strip();
			csv_writer.writerow([lang, "", id, namespace]);
	f.close();

def csv_to_raw():
	utxt = UnityText("OriginalFile/unnamed asset-resources.assets-1242.dat");
	line = "	{} | {} = {}\n";
	is_first_row = True;
	raw_data = "";
	
	f = open("localization.new.csv", "rb");
	csv_reader = csv.reader(f);
	
	for row in csv_reader:
		if is_first_row:
			raw_data += row[0] + "\n";
			is_first_row = False;
		else:
			en_lang = row[0];
			zh_lang = row[1];
			index = en_lang.find("$");
		
			if not index == -1:
				en_space_count = en_lang.count(" ", 0, index);
				zh_space_count = zh_lang.count(" ");
				zh_lang = "#" * (en_space_count - zh_space_count) +  zh_lang;

			raw_data += line.format(row[3], row[2], zh_lang);
	
	f.close();
	
	utxt.set_txt(raw_data);
	utxt.save_to_raw("FORCED/unnamed asset-resources.assets-1242.dat");
	
def gen_font_image(bmfc_filepath, output_filepath):
	# Can't add " ", make sure the path have no space.
	bmfont_tool_path = "E:\\BMFont\\bmfont.com";
	text_file_path = "\"Font\\textmin.txt\"";
	bmfc_filepath = "\"" + bmfc_filepath.replace("/", "\\") + "\"";
	output_filepath = "\"" + output_filepath.replace("/", "\\") + "\"";
	commandstr = " ".join((bmfont_tool_path , "-c" ,bmfc_filepath, "-o", output_filepath, "-t" ,text_file_path));
	os.system(commandstr.encode('mbcs'));
	
def gen_ngui_font():
	uifont = UnityUIfont("OriginalFile/unnamed asset-sharedassets0.assets-1953.dat", version = 15, is_lengacy = True);
	uifont.read_from_bmfont("Font/ForcedCalibri_0-sharedassets0.assets-18.fnt", xadvance_increasment = 1);
	uifont.save_to_raw("FORCED/unnamed asset-sharedassets0.assets-1953.dat");
	
	uifont = UnityUIfont("OriginalFile/unnamed asset-sharedassets0.assets-1954.dat", version = 15, is_lengacy = True);
	uifont.read_from_bmfont("Font/ForcedCalibri_0-sharedassets0.assets-18.fnt", xadvance_increasment = 1);
	uifont.save_to_raw("FORCED/unnamed asset-sharedassets0.assets-1954.dat");

	uifont = UnityUIfont("OriginalFile/unnamed asset-sharedassets1.assets-486.dat", version = 15, is_lengacy = True);
	uifont.read_from_bmfont("Font/ForcedCalibri_0-sharedassets0.assets-18.fnt", xadvance_increasment = 1);
	uifont.save_to_raw("FORCED/unnamed asset-sharedassets1.assets-486.dat");
	
	uifont = UnityUIfont("OriginalFile/unnamed asset-sharedassets1.assets-487.dat", version = 15, is_lengacy = True);
	uifont.read_from_bmfont("Font/ForcedArnoProSmText_0-sharedassets1.assets-90.fnt", xadvance_increasment = 1);
	uifont.save_to_raw("FORCED/unnamed asset-sharedassets1.assets-487.dat");

def gen_unity_font():
	sh = StringHelper();
	sh.code = "dos";
	sh.add_file_text("localization.new.csv");
	sh.add_western();
	sh.add_chars("\r");

	strs = "\"" + sh.get_chars() + "\""
	tool_path = "\"E:\\Python Localization Helper\\Font\\sfnttool.jar\"";
	font_path = "\"E:\\Python Localization Helper\\Font\\SourceHanSerifCN-Bold.ttf\"";
	font_export_path = "\"Font\\SourceHanSerifCN-Bold.ttf\"";
	
	commandstr = ["java -jar", tool_path, "-s", strs, font_path, font_export_path];
	os.system(" ".join(commandstr).encode('mbcs'));

	ufont = UnityFont("OriginalFile/unnamed asset-resources.assets-2052.dat", unity_version = [5, 1, 2, 0], version = 15);
	ufont.ascent += 40.0;
	ufont.convert_to_raw("FORCED/unnamed asset-resources.assets-2052.dat", "Font/SourceHanSerifCN-Bold.ttf");
	
# Gen text raw
# save_to_csv();
csv_to_raw();

# min text
sh = StringHelper();
sh.add_file_text("localization.new.csv");
sh.add_western();
f = open("Font/textmin.txt", "wb");
f.write(sh.get_chars().decode("utf-8").encode("utf-8-sig"));
f.close();

gen_font_image("Font/ForcedCalibri_0-sharedassets0.assets-18.bmfc", "Font/ForcedCalibri_0-sharedassets0.assets-18.fnt");
shutil.move("Font/ForcedCalibri_0-sharedassets0.assets-18_0.png", "FORCED/ForcedCalibri_0-sharedassets0.assets-18.png");
gen_font_image("Font/ForcedArnoProSmText_0-sharedassets1.assets-90.bmfc", "Font/ForcedArnoProSmText_0-sharedassets1.assets-90.fnt");
shutil.move("Font/ForcedArnoProSmText_0-sharedassets1.assets-90_0.png", "FORCED/ForcedArnoProSmText_0-sharedassets1.assets-90.png");

gen_ngui_font();
gen_unity_font();
