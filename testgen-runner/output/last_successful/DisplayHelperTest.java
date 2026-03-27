package displayhelper;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Locale;
import java.text.DateFormat;
import java.util.Date;

public class DisplayHelperTest {
 private DisplayHelper helper = new DisplayHelper();
 
 @Test
 public void testReturnStringList() {
 String[] list = {"Hello", "World"};
 assertEquals("Hello,World", helper.returnStringList(list));
 
 String[] singleElementArray = {"OneElement"};
 assertEquals("OneElement", helper.returnStringList(singleElementArray));
 }
 
 @Test
 public void testReturnFormattedDate() {
 Date date = new Date(); // Use current date for simplicity, can be mocked in real situation
 DateFormat formatter = DateFormat.getDateInstance(DateFormat.SHORT);
 String expectedOutput = formatter.format(date);
 
 assertEquals(expectedOutput, helper.returnFormattedDate(date));
 }
 
 @Test
 public void testGetSetMyLocale() {
 Locale locale = new Locale("en", "US"); // English (United States)
 helper.setMyLocale(locale);
 
 assertEquals(locale, helper.getMyLocale());
 }
 
 @Test
 public void testGetSetSeparator() {
 String separator = "#";
 helper.setSeparator(separator);
 
 assertEquals(separator, helper.getSeparator());
 }
}