package ch.bluepenguin.email.client.tapestry.helpers;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.Locale;
import java.util.Date;
import static org.junit.jupiter.api.Assertions.*;
import java.text.DateFormat;

public class DisplayHelperTest_v1 {
 private DisplayHelper helper; 

 @BeforeEach
 void setup() {
 helper = new DisplayHelper(); // create instance of DisplayHelper
 }

 @Test
 void testReturnFormattedDate() throws Exception {
 Date date = new Date(123L * 1000);
 Locale defaultLocaleBackup = Locale.getDefault();
 
 try {
 Locale.setDefault(Locale.US); 
 
 String expected = 
 DateFormat.getDateInstance(DateFormatSHORT, Locale.US).format(date); // corrected date format string
 
 String result = helper.returnFormattedDate(date); 
 
 assertEquals(expected, result); 
 } finally {
 Locale.setDefault(defaultLocaleBackup); 
 }
 }
}