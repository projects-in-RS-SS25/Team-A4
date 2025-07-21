import React, {useState} from "react";
import {
  Card,
  Form,
  Select,
  Radio,
  Input,
  Button,
  InputNumber,
  Divider,
  Spin
} from "antd";

const { Item: FormItem } = Form;
import {
  countries,
  accommodationTypes,
  starRatings,
  guestTypes,
  guestCountries,
  months,
} from "../consts";

const { TextArea } = Input;

const Home = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  async function onFinish(values: any) {

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
      requirement:
        values.requirement || "Please recommend me such an accommodation.",
    };

    try {
      setLoading(true);
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
      setResult(data);
    } catch (error) {
      console.error("Error fetching recommendation:", error);
      alert("Error fetching recommendation. Check the console for details.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #c3ecb2 0%, #7dd3fc 100%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        padding: "2rem",
      }}
    >
      <Card
        style={{
          maxWidth: 500,
          width: "100%",
          boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
          borderRadius: "12px",
          padding: 0,
        }}
      >
        <h2 className="text-center mb-2 text-[1.8rem] text-[#1677ff]">
          😊 Plan Your Stay
        </h2>
        <p
          style={{
            textAlign: "center",
            marginBottom: "1.5rem",
            color: "#555",
          }}
        >
          {loading ? (
          "Loading..."
          ) : result ? (
          "The recommendation result is below!"
          ) : (
          "Fill in your preferences below to get personalized accommodation recommendations."
          )}

        </p>
        {loading ? (
          <div style={{ textAlign: "center", padding: "2rem" }}>
            <Spin tip="Waiting for the LLM to generate answer..." size="large" />
          </div>
        ) : result ? (
          <div>
            <Card title="Our recommendation:">{result.response}</Card>
            <Divider>Relevant reviews</Divider>
            {result.target_reviews?.map((review: any, i: any) => (
              <Card key={i} title={review.title}>
                <p>
                  <b>Accommodation ID: </b>
                  {review.accommodation_id}
                </p>
                <p>
                  <b>Pro: </b>
                  {review.pro}
                </p>
                <p>
                  <b>Contra: </b>
                  {review.contra}
                </p>
              </Card>
            ))}
            <Divider>Other reviews</Divider>
            {result.other_reviews?.map((review: any, i: any) => (
              <Card key={i} title={review.title}>
                <p>
                  <b>Accommodation ID: </b>
                  {review.accommodation_id}
                </p>
                <p>
                  <b>Pro: </b>
                  {review.pro}
                </p>
                <p>
                  <b>Contra: </b>
                  {review.contra}
                </p>
              </Card>
            ))}
          </div>
        ) : (
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{ nights: 1 }}
        >
          <Divider orientation="left"> 🏨 Accommodation </Divider>
          <FormItem label="Type" name="accommodationType">
            <Select
              placeholder="Hotel, Apartment, etc."
              size="large"
              showSearch
            >
              {accommodationTypes.map((type) => (
                <Select.Option key={type} value={type}>
                  {type}
                </Select.Option>
              ))}
            </Select>
          </FormItem>

          <FormItem label="Country" name="accommodationCountry">
            <Select placeholder="Select Country" size="large" showSearch>
              {countries.map((country) => (
                <Select.Option key={country} value={country}>
                  {country}
                </Select.Option>
              ))}
            </Select>
          </FormItem>

          <Form.Item label="Star Rating" name="accommodationStar">
            <Select placeholder="Select Star Rating" size="large">
              {starRatings.map((star) => (
                <Select.Option key={star} value={star}>
                  {star} Stars
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Divider orientation="left"> 👥 Guests </Divider>
          <Form.Item label="Guest Type" name="guestType">
            <Select placeholder="Solo, Couple, Family" size="large">
              {guestTypes.map((type) => (
                <Select.Option key={type} value={type}>
                  {type}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item label="Guest Country" name="guestCountry">
            <Select placeholder="Your Country" size="large" showSearch>
              {guestCountries.map((country) => (
                <Select.Option key={country} value={country}>
                  {country}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Divider orientation="left"> 📍 Location Preferences </Divider>
          <FormItem label="Near Beach?" name="nearBeach">
            <Radio.Group size="large">
              <Radio.Button value={1}>Yes</Radio.Button>
              <Radio.Button value={0}>No</Radio.Button>
              <Radio.Button value={-1}>I don't care</Radio.Button>
            </Radio.Group>
          </FormItem>

          <FormItem label="Near Ski Place?" name="nearSki">
            <Radio.Group size="large">
              <Radio.Button value={1}>Yes</Radio.Button>
              <Radio.Button value={0}>No</Radio.Button>
              <Radio.Button value={-1}>I don't care</Radio.Button>
            </Radio.Group>
          </FormItem>

          <FormItem label="In Downtown?" name="inDowntown">
            <Radio.Group size="large">
              <Radio.Button value={1}>Yes</Radio.Button>
              <Radio.Button value={0}>No</Radio.Button>
              <Radio.Button value={-1}>I don't care</Radio.Button>
            </Radio.Group>
          </FormItem>

          <Divider orientation="left"> 📅 Travel Details </Divider>
          <FormItem label="Start Month" name="startMonth">
            <Select placeholder="Select Month" size="large">
              {months.map((month, i) => (
                <Select.Option key={month} value={(i + 1).toString()}>
                  {month}
                </Select.Option>
              ))}
            </Select>
          </FormItem>

          <FormItem label="Nights to Stay" name="nights">
            <InputNumber
              min={1}
              max={60}
              style={{ width: "100%" }}
              size="large"
            />
          </FormItem>

          <FormItem label="Requirements / Notes" name="requirement">
            <TextArea
              rows={4}
              placeholder="Any specific requests?"
              size="large"
            />
          </FormItem>

          <FormItem>
            <Button type="primary" htmlType="submit" block size="large">
              ✈️ Get Recommendations
            </Button>
          </FormItem>
        </Form>
        )}
      </Card>
    </div>
  );
};

export default Home;
