package stringencoder64;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class StringEncoder64Test_v1 {
 
 @Test
 void testEncodeStringUTF8() {
 assertEquals("QmFzZTY0", StringEncoder64.encodeStringUTF8("base64"));
 assertNull(StringEncoder64.encodeStringUTF8("invalid encoding"));
 }

 @Test
 void testDecodeStringUTF8() {
 try {
 assertEquals("base64", new String(StringEncoder64.decodeStringUTF8("Q[42D[K
String(StringEncoder64.decodeStringUTF8("QmFzZTY0"), "UTF-8"));
 assertThrows(Exception.class, () -> StringEncoder64.decodeStringUTF8([33D[K
StringEncoder64.decodeStringUTF8("invalid base64 string"));
 } catch (Exception e) {
 // Handle exception
 : 

It seems like there was a copy/paste error in your message and the code you[3D[K
you provided does not have any compilation errors or issues. The tests I've[4D[K
I've provided are based on the assumption that your `decode` method is thro[4D[K
throwing an IOException when it should, as indicated by your `catch (Except[7D[K
(Exception e)` clause. If this is not the case and doesn't throw an excepti[7D[K
exception in your actual codebase, please provide more information about th[2D[K
the expected behavior of these methods for further assistance.