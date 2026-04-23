package displayhelper;

import org.junit.jupiter.api.*;

import java.util.Date;
import java.text.DateFormat;
import java.util.Locale;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class DisplayHelperTest_v1 {
 private DisplayHelper displayHelper;
 
 @BeforeEach
 public void setUp() {
 displayHelper = new DisplayHelper();
 }
 
 @Test
 public void testReturnStringList() {
 String[] list = {"one", "two", "three"};
 assertEquals("one,two,three", displayHelper.returnStringList(list))[37D[K
displayHelper.returnStringList(list));
 
 list = new String[]{"only"};
 assertEquals("only", displayHelper.returnStringList(list));
 }
 
 @Test
 public void testReturnFormattedDate() {
 Date date = new Date();
 Locale locale = new Locale("en", "US");
 displayHelper.setMyLocale(locale);
 
 assertEquals(DateFormat.getDateInstance(DateFormat.SHORT, locale).f[9D[K
locale).format(date), 
 displayHelper.returnFormattedDate(date));
 }
 
 @Test
 public void testGetSetMyLocale() {
 Locale locale = new Locale("de", "DE");
 displayHelper.setMyLocale(locale);
 assertEquals(locale, displayHelper.getMyLocale());
 
 locale = new Locale("fr", "FR");
 displayHelper.setMyLocale(locale);
 assertEquals(locale, displayHelper.getMyLocale());
 }
 
 @Test
 public void testGetSetSeparator() {
 String separator = ";";
 displayHelper.setSeparator(separator);
 assertEquals(separator, displayHelper.getSeparator());
 
 separator = "|";
 displayHelper.setSeparator(separator);
 assertEquals(separator, displayHelper.getSeparator());
 }
}