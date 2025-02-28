import React, { useState } from "react";
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  Paper,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  Link,
} from "@mui/material";
import axios from "axios";

const ChatWithTravelAgent = () => {
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    { sender: "ai", message: "Seyahat önerilerinizi almak için bana bir mesaj gönderin!" },
  ]);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [travelData, setTravelData] = useState({ hotels: [] });
  const [selectedHotelDetails, setSelectedHotelDetails] = useState([]);

  const handleSendMessage = async () => {
    if (!userInput.trim()) return;
    setChatHistory((prev) => [...prev, { sender: "user", message: userInput }]);
    setLoading(true);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/openai?question=${encodeURIComponent(userInput)}`
      );

      const botMessage = "Otel seçenekleri listelendi:";
      const hotelResults = response.data.response || [];

      setChatHistory((prev) => [...prev, { sender: "ai", message: botMessage }]);
      setTravelData({ hotels: hotelResults });
    } catch (error) {
      console.error("API çağrısı başarısız:", error);
    }
    setLoading(false);
    setUserInput("");
  };

  const handleOpenDetails = async (hotel) => {
    setSelectedHotel(hotel);
    setOpenDialog(true);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/serpapi?property_token=${hotel.property_token}`
      );
      setSelectedHotelDetails(response.data);
    } catch (error) {
      console.error("Detay bilgisi alınamadı:", error);
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column", bgcolor: "#f5f5f5" }}>
      <Container maxWidth="md" sx={{ py: 4, flex: 1, display: "flex", flexDirection: "column", gap: 3 }}>
        <Typography variant="h4" sx={{ textAlign: "center", fontWeight: "bold", my: 3 }}>
          Travel Agent - Seyahat Asistanınız
        </Typography>

        <Paper elevation={3} sx={{ p: 3, height: "60vh", overflowY: "auto", bgcolor: "#ffffff", borderRadius: "16px" }}>
          {chatHistory.map((msg, index) => (
            <Box key={index} sx={{ textAlign: msg.sender === "ai" ? "left" : "right", my: 1 }}>
              <Box sx={{ display: "inline-block", bgcolor: msg.sender === "ai" ? "#e3f2fd" : "#c8e6c9", p: 2, borderRadius: "12px" }}>
                <Typography sx={{ fontSize: "16px" }}>{msg.message}</Typography>
              </Box>
            </Box>
          ))}

          {travelData.hotels.length > 0 && (
            <TableContainer component={Paper} sx={{ mt: 3, borderRadius: "12px" }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell><b>Otel Adı</b></TableCell>
                    <TableCell><b>Toplam Fiyat</b></TableCell>
                    <TableCell><b>Vergiler Dahil Fiyat</b></TableCell>
                    <TableCell><b>Puan</b></TableCell>
                    <TableCell><b>Yıldız</b></TableCell>
                    <TableCell><b>Detaylar</b></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {travelData.hotels.map((hotel, index) => (
                    <TableRow key={index}>
                      <TableCell>{hotel.hotel_name}</TableCell>
                      <TableCell>{hotel.total_price_without_tax}</TableCell>
                      <TableCell>{hotel.total_price_with_tax}</TableCell>
                      <TableCell>{hotel.rating} ⭐</TableCell>
                      <TableCell>{hotel.hotel_class}</TableCell>
                      <TableCell>
                        <Button variant="contained" size="small" onClick={() => handleOpenDetails(hotel)}>
                          Detaylar
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>

        <Paper elevation={3} sx={{ p: 3, display: "flex", gap: 2, borderRadius: "12px" }}>
          <TextField 
            label="Bir mesaj yazın..." 
            variant="outlined" 
            fullWidth 
            value={userInput} 
            onChange={(e) => setUserInput(e.target.value)} 
            onKeyDown={(e) => e.key === "Enter" && handleSendMessage()} 
          />
          <Button variant="contained" color="primary" onClick={handleSendMessage} disabled={loading}>
            {loading ? <CircularProgress size={24} color="inherit" /> : "GÖNDER"}
          </Button>
        </Paper>
      </Container>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="lg" fullWidth>
        <DialogTitle>Otel Detayları</DialogTitle>
        <DialogContent sx={{ width: "90vw", padding: 3 }}>
          {selectedHotel && (
            <>
              <Typography variant="h6">{selectedHotel.hotel_name}</Typography>
              <Typography><b>Toplam Fiyat:</b> {selectedHotel.total_price_without_tax}</Typography>
              <Typography><b>Vergiler Dahil Fiyat:</b> {selectedHotel.total_price_with_tax}</Typography>
              <Typography><b>Puan:</b> {selectedHotel.rating} ⭐</Typography>
              <Typography><b>Yıldız:</b> {selectedHotel.hotel_class}</Typography>

              {selectedHotelDetails.length > 0 && (
                <TableContainer component={Paper} sx={{ mt: 3, minWidth: "800px" }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell><b>Acenta</b></TableCell>
                        <TableCell><b>Günlük Fiyat</b></TableCell>
                        <TableCell><b>Vergiler Dahil Günlük</b></TableCell>
                        <TableCell><b>Toplam Fiyat</b></TableCell>
                        <TableCell><b>Vergiler Dahil Toplam</b></TableCell>
                        <TableCell><b>Bağlantı</b></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedHotelDetails.map((detail, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            <img src={detail.logo} alt={detail.source} width="40" height="40" style={{ marginRight: 10 }} />
                            {detail.source}
                          </TableCell>
                          <TableCell>{detail.lowest_daily_without_tax}</TableCell>
                          <TableCell>{detail.lowest_daily_with_tax}</TableCell>
                          <TableCell>{detail.total_price_without_tax}</TableCell>
                          <TableCell>{detail.total_price_with_tax}</TableCell>
                          <TableCell>
                            <Link href={detail.link} target="_blank" rel="noopener">Rezervasyon</Link>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default ChatWithTravelAgent;
