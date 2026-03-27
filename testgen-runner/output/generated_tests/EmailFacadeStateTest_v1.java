package emailfacadestate;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class EmailFacadeStateTest_v1 {
 private EmailFacadeState emailFacadeState;
 
 @BeforeEach
 public void setup() {
 emailFacadeState = new EmailFacadeState();
 }

 @Test
 public void testClearShouldEmptyTheHashMap() {
 emailFacadeState.setState(1, true);
 emailFacadeState.clear();
 
 assertTrue(emailFacadeState.isAllClean()); // Check if all states are clean after clear
 }
}