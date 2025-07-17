import React from 'react';
import { Card, Form, Select, Radio, Input, Button, InputNumber, Divider } from 'antd';

const { TextArea } = Input;

const Home = () => {
  const [form] = Form.useForm();

  const onFinish = async (values) => {
    console.log('Form submitted with values:', JSON.stringify(values, null, 2));

    // Transform Keys to Match Backend
    const payload = {
        accommodation_country: values.accommodationCountry,
        accommodation_type: [values.accommodationType],
        accommodation_star: parseFloat(values.accommodationStar || -1),
        ski: values.nearSki ?? -1,
        beach: values.nearBeach ?? -1,
        center: values.inDowntown ?? -1,
        score: -1,
        guest_type: values.guestType,
        guest_country: values.guestCountry,
        months: parseInt(values.startMonth || -1),
        nights: parseInt(String(values.nights || -1)),
        requirement: values.requirement || "Please recommend me such an accommodation."
    };

    try {
        const response = await fetch("http://127.0.0.1:5001/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Recommendation response:", data);
        alert("Recommendation fetched successfully! Check the console.");
    } catch (error) {
        console.error("Error fetching recommendation:", error);
        alert("Error fetching recommendation. Check the console for details.");
    }
};



  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #c3ecb2 0%, #7dd3fc 100%)",
      display: "flex",
      justifyContent: "center",
      alignItems: "flex-start",
      padding: "2rem"
    }}>
      <Card
        style={{
          maxWidth: 500,
          width: "100%",
          boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
          borderRadius: "12px",
          padding: 0
        }}
        bodyStyle={{ padding: "1.5rem" }}
      >
        <h2 style={{
          textAlign: "center",
          marginBottom: "0.5rem",
          fontSize: "1.8rem",
          color: "#1677ff"
        }}>
          😊 Plan Your Stay
        </h2>
        <p style={{
          textAlign: "center",
          marginBottom: "1.5rem",
          color: "#555"
        }}>
          Fill in your preferences below to get personalized accommodation recommendations.
        </p>

        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{ nights: 1 }}
        >
          <Divider orientation="left"> 🏨 Accommodation </Divider>
          <Form.Item label="Type" name="accommodationType">
            <Select placeholder="Hotel, Apartment, etc." size="large" showSearch>
              {[
                'Hotel', 'Bed and Breakfast', 'ApartHotel', 'Hostel', 'Resort', 'Apartment',
                'Motel', 'Guest house', 'Farm stay', 'Lodge', 'Villa', 'Camping', 'Capsule Hotel',
                'Inn', 'Holiday home', 'Homestay', 'Chalet', 'Ryokan', 'Holiday Park',
                'Country house', 'Boat', 'Tented camp', 'Student accommodation', 'Riad', 'Cruise',
                'Love Hotel', 'Japanese-style Business Hotel'
              ].map((type) => (
                <Select.Option key={type} value={type}>{type}</Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item label="Country" name="accommodationCountry">
            <Select placeholder="Select Country" size="large" showSearch>
              {[
                'Australia', 'South Africa', 'New Zealand', 'United States of America', 'Italy',
                'Canada', 'Spain', 'Bolivia', 'Georgia', 'Egypt', 'Cook Islands', 'Greece',
                'Poland', 'Belgium', 'United Kingdom', 'Austria', 'India', 'Turkey', 'Germany',
                'Vietnam', 'United Arab Emirates', 'Bulgaria', 'Malta', 'Portugal', 'Japan',
                'Malaysia', 'Colombia', 'Thailand', 'France', 'Tanzania', 'Netherlands',
                'Saudi Arabia', 'Croatia', 'Indonesia', 'Philippines', 'Qatar', 'Singapore',
                'Estonia', 'Denmark', 'Taiwan', 'Korea, South', 'Costa Rica', 'Israel',
                'Norway', 'Czech Republic', 'Finland', 'Hungary', 'Rwanda', 'Switzerland',
                'Lebanon', 'Iceland', 'Hong Kong', 'Panama', 'Ireland', 'Morocco',
                'Bosnia and Herzegovina', 'Iraq', 'Mexico', 'Pakistan', 'Nepal', 'Slovenia',
                'Brazil', 'Ethiopia', 'Serbia', 'Uganda', 'Armenia', 'Oman', 'Aruba',
                'Montenegro', 'Grenada', 'Romania', 'Cyprus', 'Bahrain', 'Bangladesh',
                'Cambodia', 'Maldives', 'Azerbaijan', 'Argentina', 'Sweden', 'Albania',
                'Lithuania', 'Andorra', 'Puerto Rico', 'China', 'Jordan', 'Sri Lanka',
                'Jamaica', 'Macedonia', 'Slovakia', 'Barbados', 'Uzbekistan', 'Peru',
                'Mongolia', 'Mauritius', 'Chile', 'Kenya', 'Seychelles', 'Latvia', 'Laos',
                'Saint Vincent and the Grenadines', 'Guatemala', 'Belize', 'Ukraine',
                'Northern Cyprus', 'Nicaragua', 'Tunisia', 'Honduras', 'Bermuda',
                'Trinidad and Tobago', 'Antigua and Barbuda', 'Samoa', 'Fiji', 'Ecuador',
                'Kosovo', 'El Salvador', 'Luxembourg', 'Kyrgyzstan', 'Uruguay', 'Macau',
                'Swaziland', 'Senegal', 'Moldova', 'Venezuela', 'Kuwait', 'Saint Martin',
                'Namibia', 'Dominican Republic', 'Zambia', 'Zimbabwe', 'Nigeria',
                'Kazakhstan', 'French Polynesia', 'Saint Lucia', 'Tonga', 'Vanuatu',
                'Botswana', 'Curaçao', 'New Caledonia', 'Mozambique', 'Liechtenstein',
                'Monaco', 'Bonaire, Saint Eustatius and Saba', 'Ghana', 'Gibraltar',
                'San Marino', 'Madagascar', 'Djibouti', 'Myanmar', 'Virgin Islands, U.S.',
                'Palestine', 'Guam', 'Reunion', 'Bahamas', 'Brunei Darussalam',
                'Papua New Guinea', 'Suriname', 'Benin', 'Turks and Caicos Islands',
                'Faroe Islands', 'Dominica', 'Gambia', 'Cape Verde', 'Bhutan', 'Greenland',
                'Malawi', 'Algeria', 'Burundi', 'Paraguay', 'Angola', 'Solomon Islands',
                'Cayman Islands', 'Tajikistan', 'Cote d\'Ivoire', 'Haiti', 'Isle of Man',
                'Sao Tome and Principe', 'Guadeloupe', 'Togo', 'Norfolk Island', 'Palau'
              ].map((country) => (
                <Select.Option key={country} value={country}>{country}</Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item label="Star Rating" name="accommodationStar">
            <Select placeholder="Select Star Rating" size="large">
              {['0.0', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0'].map((star) => (
                <Select.Option key={star} value={star}>{star} Stars</Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Divider orientation="left"> 👥 Guests </Divider>
          <Form.Item label="Guest Type" name="guestType">
            <Select placeholder="Solo, Couple, Family" size="large">
              {['Couple', 'Family with children', 'Solo traveller', 'Group'].map((type) => (
                <Select.Option key={type} value={type}>{type}</Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item label="Guest Country" name="guestCountry">
            <Select placeholder="Your Country" size="large" showSearch>
              {[
                'Zuc', 'Made', 'Xazas', 'Nukeye', 'Mejok', 'Kiy', 'Qehoj', 'Nen', 'Vey', 'Vig',
                'Keyu', 'Tuhi', 'Fanir', 'Pule', 'Dow', 'Pihay', 'Modey', 'Ciqo', 'Guroz', 'Vema',
                'Tucit', 'Heyuru', 'Buzi', 'Fuxa', 'Jof', 'May', 'Wapef', 'Vezuz', 'Kecuk',
                // ... add all guest countries you have ...
              ].map((country) => (
                <Select.Option key={country} value={country}>{country}</Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Divider orientation="left"> 📍 Location Preferences </Divider>
          <Form.Item label="Near Beach?" name="nearBeach">
            <Radio.Group size="large">
              <Radio.Button value={1}>Yes</Radio.Button>
              <Radio.Button value={0}>No</Radio.Button>
              <Radio.Button value={-1}>I don't care</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="Near Ski Place?" name="nearSki">
            <Radio.Group size="large">
              <Radio.Button value={1}>Yes</Radio.Button>
              <Radio.Button value={0}>No</Radio.Button>
              <Radio.Button value={-1}>I don't care</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="In Downtown?" name="inDowntown">
            <Radio.Group size="large">
              <Radio.Button value={1}>Yes</Radio.Button>
              <Radio.Button value={0}>No</Radio.Button>
              <Radio.Button value={-1}>I don't care</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Divider orientation="left"> 📅 Travel Details </Divider>
          <Form.Item label="Start Month" name="startMonth">
            <Select placeholder="Select Month" size="large">
              {[
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
              ].map((month, i) => (
                <Select.Option key={month} value={(i + 1).toString()}>{month}</Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item label="Nights to Stay" name="nights">
            <InputNumber min={1} max={60} style={{ width: "100%" }} size="large" />
          </Form.Item>

          <Form.Item label="Requirements / Notes" name="requirement">
            <TextArea rows={4} placeholder="Any specific requests?" size="large" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large">
              ✈️ Get Recommendations
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Home;
