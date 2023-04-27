# FP-Growth-in-Python
Coding FP-Growth in python from scratch


import javax.crypto.*;
import javax.crypto.spec.*;

public class DesxDecryption {
    
    public static void main(String[] args) throws Exception {
        byte[] keyBytes = "secretkey".getBytes();
        byte[] ivBytes = "initializ".getBytes();
        byte[] ciphertext = new byte[] {...}; // replace with actual ciphertext
        
        // Create DES key from first 8 bytes of keyBytes
        DESKeySpec desKeySpec = new DESKeySpec(keyBytes, 0);
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
        SecretKey desKey = keyFactory.generateSecret(desKeySpec);
        
        // Create DESX key from keyBytes
        byte[] desxKeyBytes = new byte[24];
        System.arraycopy(keyBytes, 0, desxKeyBytes, 0, 8);
        System.arraycopy(keyBytes, 0, desxKeyBytes, 8, 8);
        System.arraycopy(keyBytes, 0, desxKeyBytes, 16, 8);
        SecretKeySpec desxKeySpec = new SecretKeySpec(desxKeyBytes, "DESede");
        
        // Create cipher using DESX key and IV
        Cipher cipher = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, desxKeySpec, new IvParameterSpec(ivBytes));
        
        // Decrypt ciphertext
        byte[] plaintext = cipher.doFinal(ciphertext);
        System.out.println(new String(plaintext));
    }
}
