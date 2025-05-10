import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class ISPDetailsFinder {

    // Function to get ISP details for a single IP address
    private static String getIspDetails(String ip) {
        try {
            String url = "http://ip-api.com/json/" + ip;
            HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);

            int status = connection.getResponseCode();
            if (status != 200) {
                return "Error: Unable to fetch data for IP " + ip;
            }

            // Read the response and parse ISP details
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }

                String responseStr = response.toString();
                if (responseStr.contains("\"status\":\"fail\"")) {
                    return "Error: Could not retrieve ISP details for IP " + ip;
                }

                // Extracting the needed details from the JSON response
                String isp = responseStr.split("\"isp\":\"")[1].split("\"")[0];
                String org = responseStr.split("\"org\":\"")[1].split("\"")[0];
                String city = responseStr.split("\"city\":\"")[1].split("\"")[0];
                String region = responseStr.split("\"regionName\":\"")[1].split("\"")[0];
                String country = responseStr.split("\"country\":\"")[1].split("\"")[0];
                String as = responseStr.split("\"as\":\"")[1].split("\"")[0];

                return String.format("IP: %s\nISP: %s\nOrganization: %s\nLocation: %s, %s, %s\nAS: %s\n", ip, isp, org, city, region, country, as);
            }
        } catch (Exception e) {
            return "Error: Could not retrieve ISP details for IP " + ip + " (" + e.getMessage() + ")";
        }
    }

    // Function to get ISP details for multiple IP addresses from a file
    private static String getIspDetailsFromFile(String filePath) {
        StringBuilder result = new StringBuilder();
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filePath));
            String ip;
            while ((ip = reader.readLine()) != null) {
                result.append(getIspDetails(ip)).append("\n").append("-".repeat(30)).append("\n");
            }
            reader.close();
        } catch (IOException e) {
            return "Error: Could not read the file (" + e.getMessage() + ")";
        }
        return result.toString();
    }

    // Main function to create the GUI and handle user interactions
    public static void main(String[] args) {
        // Frame
        JFrame frame = new JFrame("ISP Details Finder");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 450);
        frame.setLayout(new BorderLayout(10, 10));

        // Title Label
        JLabel titleLabel = new JLabel("ISP Details Finder", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        frame.add(titleLabel, BorderLayout.NORTH);

        // Main Panel
        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints constraints = new GridBagConstraints();
        constraints.insets = new Insets(10, 10, 10, 10);
        frame.add(panel, BorderLayout.CENTER);

        // Single IP input
        JLabel ipLabel = new JLabel("Enter IP Address:");
        constraints.gridx = 0;
        constraints.gridy = 0;
        panel.add(ipLabel, constraints);

        JTextField ipField = new JTextField(30);
        constraints.gridx = 1;
        panel.add(ipField, constraints);

        // Search button for single IP
        JButton searchButton = new JButton("Search Single IP");
        constraints.gridx = 0;
        constraints.gridy = 1;
        constraints.gridwidth = 2;
        panel.add(searchButton, constraints);

        // File chooser button
        JButton fileButton = new JButton("Choose File with IPs");
        constraints.gridy = 2;
        panel.add(fileButton, constraints);

        // Result Text Area
        JTextArea resultArea = new JTextArea(10, 50);
        resultArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(resultArea);
        frame.add(scrollPane, BorderLayout.SOUTH);

        // Action listeners for buttons
        searchButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String ip = ipField.getText().trim();
                if (!ip.isEmpty()) {
                    String ispDetails = getIspDetails(ip);
                    resultArea.setText(ispDetails);
                } else {
                    JOptionPane.showMessageDialog(frame, "Please enter an IP address", "Input Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });

        fileButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setDialogTitle("Select a File with IPs");
                int result = fileChooser.showOpenDialog(frame);
                if (result == JFileChooser.APPROVE_OPTION) {
                    File selectedFile = fileChooser.getSelectedFile();
                    String ispDetails = getIspDetailsFromFile(selectedFile.getAbsolutePath());
                    resultArea.setText(ispDetails);
                }
            }
        });

        // Show the frame
        frame.setVisible(true);
    }
}
