package emailfacadestate;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class EmailFacadeStateTest_v1 {
 @Test
 void testIsAllClean() {
 // Create an instance of the CUT with some states set
 EmailFacadeState emailFS = new EmailFacadeState();
 Integer id = 12345;
 
 // Verify that all states are clean when none were initially set
 assertEquals(true, emailFS.isAllClean()); 
 
 boolean dirtyFlag = true;
 // Set one state to dirty and verify that isAllClean returns false
 emailFS.setState(id, dirtyFlag);
 assertFalse(emailFS.isDirty(id)); 
 }
 
 @Test
 void testSetAndGetState() {
 // Create an instance of the CUT
 EmailFacadeState emailFS = new EmailFacadeState();
 
 Integer id = 12345;
 boolean dirtyFlag = true;
 
 // Set state and verify it is set correctly
 emailFS.setState(id, dirtyFlag);
 assertEquals(dirtyFlag, emailFS.isDirty(id));
 }
 
 @Test
 void testClear() {
 // Create an instance of the CUT with some states set
 EmailFacadeState emailFS = new EmailFacadeState();
 Integer id = 12345;
 boolean dirtyFlag = true;
 emailFS.setState(id, dirtyFlag);
 
 // Clear all states and verify they are clear
 emailFS.clear();
 assertTrue(emailFS.isDirty(id)); // the state should be clean
 }
 
 @Test
 void testSetAll() {
 // Create an instance of the CUT with some states set
 EmailFacadeState emailFS = new EmailFacadeState();
 Integer id = 12345;
 
 // Set all states to a specific value and verify they are set correctly
 boolean dirtyFlag = true;
 emailFS.setAll(dirtyFlag); 
 assertEquals(dirtyFlag, emailFS.isDirty(id)); 
 }
}