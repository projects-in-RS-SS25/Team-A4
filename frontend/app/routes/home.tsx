import React, { useState } from "react";
import type { Route } from "./+types/home";
import { Button, Input, InputNumber, Select, Radio, Spin, Form, Card, Divider } from 'antd';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Accommodation Recommendation System" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <UserInput />;
}

function UserInput() {
  const [result, setResult] = useState<any>(null);
  const [currentPage, setCurrentPage] = useState<"form" | "result" | "loading">("form");
  const handleFinish = async (values: any) => {
    console.log("All values: ", values);
    try {
      setCurrentPage("loading");
      const response = await fetch("http://localhost:5001/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      if (!response.ok) throw new Error("Error with API");
      const result = await response.json();
      console.log("Result: ", result);
      setResult(result as Answer);
      setCurrentPage("result");
    } catch (error) {
      console.error(error);
    }

  };
  return (<main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        {currentPage === "form" && (
        <Form
          name="wrap"
          labelCol={{ flex: '300px' }}
          labelAlign="left"
          labelWrap
          wrapperCol={{ flex: 1 }}
          colon={false}
          style={{ maxWidth: 1000 }}
          onFinish={handleFinish}
        >
        <Form.Item label="Accommodation type: " name="accommodation_type">
          <Select
      showSearch
      style={{ width: 250 }}
      options={[
        { value: 'Hotel', label: 'Hotel' },
        { value: 'Bed and Breakfast', label: 'Bed and Breakfast' },
        { value: 'ApartHotel', label: 'ApartHotel' },
        { value: 'Hostel', label: 'Hostel' },
        { value: 'Resort', label: 'Resort' },
        { value: 'Apartment', label: 'Apartment' },
        { value: 'Motel', label: 'Motel' },
        { value: 'Guest house', label: 'Guest house' },
        { value: 'Farm stay', label: 'Farm stay' },
        { value: 'Lodge', label: 'Lodge' },
        { value: 'Villa', label: 'Villa' },
        { value: 'Camping', label: 'Camping' },
        { value: 'Capsule Hotel', label: 'Capsule Hotel' },
        { value: 'Inn', label: 'Inn' },
        { value: 'Holiday home', label: 'Holiday home' },
        { value: 'Homestay', label: 'Homestay' },
        { value: 'Chalet', label: 'Chalet' },
        { value: 'Ryokan', label: 'Ryokan' },
        { value: 'Holiday Park', label: 'Holiday Park' },
        { value: 'Country house', label: 'Country house' },
        { value: 'Boat', label: 'Boat' },
        { value: 'Tented camp', label: 'Tented camp' },
        { value: 'Student accommodation', label: 'Student accommodation' },
        { value: 'Riad', label: 'Riad' },
        { value: 'Cruise', label: 'Cruise' },
        { value: 'Love Hotel', label: 'Love Hotel' },
        { value: 'Japanese-style Business Hotel', label: 'Japanese-style Business Hotel' },
        ]}
          />
        </Form.Item>
        <Form.Item label="Accommodation country: " name="accommodation_country">
          <Select
            showSearch
            style={{ width: 250 }}
            options={[
            { value: 'Australia', label: 'Australia' },
            { value: 'South Africa', label: 'South Africa' },
            { value: 'New Zealand', label: 'New Zealand' },
{ value: 'United States of America', label: 'United States of America' },
{ value: 'Italy', label: 'Italy' },
{ value: 'Canada', label: 'Canada' },
{ value: 'Spain', label: 'Spain' },
{ value: 'Bolivia', label: 'Bolivia' },
{ value: 'Georgia', label: 'Georgia' },
{ value: 'Egypt', label: 'Egypt' },
{ value: 'Cook Islands', label: 'Cook Islands' },
{ value: 'Greece', label: 'Greece' },
{ value: 'Poland', label: 'Poland' },
{ value: 'Belgium', label: 'Belgium' },
{ value: 'United Kingdom', label: 'United Kingdom' },
{ value: 'Austria', label: 'Austria' },
{ value: 'India', label: 'India' },
{ value: 'Turkey', label: 'Turkey' },
{ value: 'Germany', label: 'Germany' },
{ value: 'Vietnam', label: 'Vietnam' },
{ value: 'United Arab Emirates', label: 'United Arab Emirates' },
{ value: 'Bulgaria', label: 'Bulgaria' },
{ value: 'Malta', label: 'Malta' },
{ value: 'Portugal', label: 'Portugal' },
{ value: 'Japan', label: 'Japan' },
{ value: 'Malaysia', label: 'Malaysia' },
{ value: 'Colombia', label: 'Colombia' },
{ value: 'Thailand', label: 'Thailand' },
{ value: 'France', label: 'France' },
{ value: 'Tanzania', label: 'Tanzania' },
{ value: 'Netherlands', label: 'Netherlands' },
{ value: 'Saudi Arabia', label: 'Saudi Arabia' },
{ value: 'Croatia', label: 'Croatia' },
{ value: 'Indonesia', label: 'Indonesia' },
{ value: 'Philippines', label: 'Philippines' },
{ value: 'Qatar', label: 'Qatar' },
{ value: 'Singapore', label: 'Singapore' },
{ value: 'Estonia', label: 'Estonia' },
{ value: 'Denmark', label: 'Denmark' },
{ value: 'Taiwan', label: 'Taiwan' },
{ value: 'Korea, South', label: 'Korea, South' },
{ value: 'Costa Rica', label: 'Costa Rica' },
{ value: 'Israel', label: 'Israel' },
{ value: 'Norway', label: 'Norway' },
{ value: 'Czech Republic', label: 'Czech Republic' },
{ value: 'Finland', label: 'Finland' },
{ value: 'Hungary', label: 'Hungary' },
{ value: 'Rwanda', label: 'Rwanda' },
{ value: 'Switzerland', label: 'Switzerland' },
{ value: 'Lebanon', label: 'Lebanon' },
{ value: 'Iceland', label: 'Iceland' },
{ value: 'Hong Kong', label: 'Hong Kong' },
{ value: 'Panama', label: 'Panama' },
{ value: 'Ireland', label: 'Ireland' },
{ value: 'Morocco', label: 'Morocco' },
{ value: 'Bosnia and Herzegovina', label: 'Bosnia and Herzegovina' },
{ value: 'Iraq', label: 'Iraq' },
{ value: 'Mexico', label: 'Mexico' },
{ value: 'Pakistan', label: 'Pakistan' },
{ value: 'Nepal', label: 'Nepal' },
{ value: 'Slovenia', label: 'Slovenia' },
{ value: 'Brazil', label: 'Brazil' },
{ value: 'Ethiopia', label: 'Ethiopia' },
{ value: 'Serbia', label: 'Serbia' },
{ value: 'Uganda', label: 'Uganda' },
{ value: 'Armenia', label: 'Armenia' },
{ value: 'Oman', label: 'Oman' },
{ value: 'Aruba', label: 'Aruba' },
{ value: 'Montenegro', label: 'Montenegro' },
{ value: 'Grenada', label: 'Grenada' },
{ value: 'Romania', label: 'Romania' },
{ value: 'Cyprus', label: 'Cyprus' },
{ value: 'Bahrain', label: 'Bahrain' },
{ value: 'Bangladesh', label: 'Bangladesh' },
{ value: 'Cambodia', label: 'Cambodia' },
{ value: 'Maldives', label: 'Maldives' },
{ value: 'Azerbaijan', label: 'Azerbaijan' },
{ value: 'Argentina', label: 'Argentina' },
{ value: 'Sweden', label: 'Sweden' },
{ value: 'Albania', label: 'Albania' },
{ value: 'Lithuania', label: 'Lithuania' },
{ value: 'Andorra', label: 'Andorra' },
{ value: 'Puerto Rico', label: 'Puerto Rico' },
{ value: 'China', label: 'China' },
{ value: 'Jordan', label: 'Jordan' },
{ value: 'Sri Lanka', label: 'Sri Lanka' },
{ value: 'Jamaica', label: 'Jamaica' },
{ value: 'Macedonia', label: 'Macedonia' },
{ value: 'Slovakia', label: 'Slovakia' },
{ value: 'Barbados', label: 'Barbados' },
{ value: 'Uzbekistan', label: 'Uzbekistan' },
{ value: 'Peru', label: 'Peru' },
{ value: 'Mongolia', label: 'Mongolia' },
{ value: 'Mauritius', label: 'Mauritius' },
{ value: 'Chile', label: 'Chile' },
{ value: 'Kenya', label: 'Kenya' },
{ value: 'Seychelles', label: 'Seychelles' },
{ value: 'Latvia', label: 'Latvia' },
{ value: 'Laos', label: 'Laos' },
{ value: 'Saint Vincent and the Grenadines', label: 'Saint Vincent and the Grenadines' },
{ value: 'Guatemala', label: 'Guatemala' },
{ value: 'Belize', label: 'Belize' },
{ value: 'Ukraine', label: 'Ukraine' },
{ value: 'Northern Cyprus', label: 'Northern Cyprus' },
{ value: 'Nicaragua', label: 'Nicaragua' },
{ value: 'Tunisia', label: 'Tunisia' },
{ value: 'Honduras', label: 'Honduras' },
{ value: 'Bermuda', label: 'Bermuda' },
{ value: 'Trinidad and Tobago', label: 'Trinidad and Tobago' },
{ value: 'Antigua and Barbuda', label: 'Antigua and Barbuda' },
{ value: 'Samoa', label: 'Samoa' },
{ value: 'Fiji', label: 'Fiji' },
{ value: 'Ecuador', label: 'Ecuador' },
{ value: 'Kosovo', label: 'Kosovo' },
{ value: 'El Salvador', label: 'El Salvador' },
{ value: 'Luxembourg', label: 'Luxembourg' },
{ value: 'Kyrgyzstan', label: 'Kyrgyzstan' },
{ value: 'Uruguay', label: 'Uruguay' },
{ value: 'Macau', label: 'Macau' },
{ value: 'Swaziland', label: 'Swaziland' },
{ value: 'Senegal', label: 'Senegal' },
{ value: 'Moldova', label: 'Moldova' },
{ value: 'Venezuela', label: 'Venezuela' },
{ value: 'Kuwait', label: 'Kuwait' },
{ value: 'Saint Martin', label: 'Saint Martin' },
{ value: 'Namibia', label: 'Namibia' },
{ value: 'Dominican Republic', label: 'Dominican Republic' },
{ value: 'Zambia', label: 'Zambia' },
{ value: 'Zimbabwe', label: 'Zimbabwe' },
{ value: 'Nigeria', label: 'Nigeria' },
{ value: 'Kazakhstan', label: 'Kazakhstan' },
{ value: 'French Polynesia', label: 'French Polynesia' },
{ value: 'Saint Lucia', label: 'Saint Lucia' },
{ value: 'Tonga', label: 'Tonga' },
{ value: 'Vanuatu', label: 'Vanuatu' },
{ value: 'Botswana', label: 'Botswana' },
{ value: 'Curaçao', label: 'Curaçao' },
{ value: 'New Caledonia', label: 'New Caledonia' },
{ value: 'Mozambique', label: 'Mozambique' },
{ value: 'Liechtenstein', label: 'Liechtenstein' },
{ value: 'Monaco', label: 'Monaco' },
{ value: 'Bonaire, Saint Eustatius and Saba', label: 'Bonaire, Saint Eustatius and Saba' },
{ value: 'Ghana', label: 'Ghana' },
{ value: 'Gibraltar', label: 'Gibraltar' },
{ value: 'San Marino', label: 'San Marino' },
{ value: 'Madagascar', label: 'Madagascar' },
{ value: 'Djibouti', label: 'Djibouti' },
{ value: 'Myanmar', label: 'Myanmar' },
{ value: 'Virgin Islands, U.S.', label: 'Virgin Islands, U.S.' },
{ value: 'Palestine', label: 'Palestine' },
{ value: 'Guam', label: 'Guam' },
{ value: 'Reunion', label: 'Reunion' },
{ value: 'Bahamas', label: 'Bahamas' },
{ value: 'Brunei Darussalam', label: 'Brunei Darussalam' },
{ value: 'Papua New Guinea', label: 'Papua New Guinea' },
{ value: 'Suriname', label: 'Suriname' },
{ value: 'Benin', label: 'Benin' },
{ value: 'Turks and Caicos Islands', label: 'Turks and Caicos Islands' },
{ value: 'Faroe Islands', label: 'Faroe Islands' },
{ value: 'Dominica', label: 'Dominica' },
{ value: 'Gambia', label: 'Gambia' },
{ value: 'Cape Verde', label: 'Cape Verde' },
{ value: 'Bhutan', label: 'Bhutan' },
{ value: 'Greenland', label: 'Greenland' },
{ value: 'Malawi', label: 'Malawi' },
{ value: 'Algeria', label: 'Algeria' },
{ value: 'Burundi', label: 'Burundi' },
{ value: 'Paraguay', label: 'Paraguay' },
{ value: 'Angola', label: 'Angola' },
{ value: 'Solomon Islands', label: 'Solomon Islands' },
{ value: 'Cayman Islands', label: 'Cayman Islands' },
{ value: 'Tajikistan', label: 'Tajikistan' },
{ value: 'Cote d\'Ivoire', label: 'Cote d\'Ivoire' },
{ value: 'Haiti', label: 'Haiti' },
{ value: 'Isle of Man', label: 'Isle of Man' },
{ value: 'Sao Tome and Principe', label: 'Sao Tome and Principe' },
{ value: 'Guadeloupe', label: 'Guadeloupe' },
{ value: 'Togo', label: 'Togo' },
{ value: 'Norfolk Island', label: 'Norfolk Island' },
      { value: 'Palau', label: 'Palau' },        
            ]}
          />
        </Form.Item>
        <Form.Item label="Accommodation star: " name="accommodation_star">
          <Select
      showSearch
      style={{ width: 250 }}
      options={[
{ value: '0.0', label: '0.0' },
{ value: '1.0', label: '1.0' },
{ value: '1.5', label: '1.5' },
{ value: '2.0', label: '2.0' },
{ value: '2.5', label: '2.5' },
{ value: '3.0', label: '3.0' },
{ value: '3.5', label: '3.5' },
{ value: '4.0', label: '4.0' },
{ value: '4.5', label: '4.5' },
{ value: '5.0', label: '5.0' },
        ]}
    />
        </Form.Item>
        <Form.Item label="Guest type: " name="guest_type">
          <Select
      showSearch
      style={{ width: 250 }}
      options={[
{ value: 'Couple', label: 'Couple' },
{ value: 'Family with children', label: 'Family with children' },
{ value: 'Solo traveller', label: 'Solo traveller' },
{ value: 'Group', label: 'Group' },
        ]}
    />
        </Form.Item>
        <Form.Item label="Guest country: " name="guest_country">
          <Select
      showSearch
      style={{ width: 250 }}
      options={[
{ value: 'Zuc', label: 'Zuc' },
{ value: 'Made', label: 'Made' },
{ value: 'Xazas', label: 'Xazas' },
{ value: 'Nukeye', label: 'Nukeye' },
{ value: 'Mejok', label: 'Mejok' },
{ value: 'Kiy', label: 'Kiy' },
{ value: 'Qehoj', label: 'Qehoj' },
{ value: 'Nen', label: 'Nen' },
{ value: 'Vey', label: 'Vey' },
{ value: 'Vig', label: 'Vig' },
{ value: 'Keyu', label: 'Keyu' },
{ value: 'Tuhi', label: 'Tuhi' },
{ value: 'Fanir', label: 'Fanir' },
{ value: 'Pule', label: 'Pule' },
{ value: 'Dow', label: 'Dow' },
{ value: 'Pihay', label: 'Pihay' },
{ value: 'Modey', label: 'Modey' },
{ value: 'Ciqo', label: 'Ciqo' },
{ value: 'Guroz', label: 'Guroz' },
{ value: 'Vema', label: 'Vema' },
{ value: 'Tucit', label: 'Tucit' },
{ value: 'Heyuru', label: 'Heyuru' },
{ value: 'Buzi', label: 'Buzi' },
{ value: 'Fuxa', label: 'Fuxa' },
{ value: 'Jof', label: 'Jof' },
{ value: 'May', label: 'May' },
{ value: 'Wapef', label: 'Wapef' },
{ value: 'Vezuz', label: 'Vezuz' },
{ value: 'Kecuk', label: 'Kecuk' },
{ value: 'Pimes', label: 'Pimes' },
{ value: 'Cutip', label: 'Cutip' },
{ value: 'Tuleho', label: 'Tuleho' },
{ value: 'Naz', label: 'Naz' },
{ value: 'Tig', label: 'Tig' },
{ value: 'Qebuf', label: 'Qebuf' },
{ value: 'Faxul', label: 'Faxul' },
{ value: 'Vegeve', label: 'Vegeve' },
{ value: 'Sajeb', label: 'Sajeb' },
{ value: 'Rixo', label: 'Rixo' },
{ value: 'Bemil', label: 'Bemil' },
{ value: 'Gozowa', label: 'Gozowa' },
{ value: 'Kudefa', label: 'Kudefa' },
{ value: 'Xaye', label: 'Xaye' },
{ value: 'Pikune', label: 'Pikune' },
{ value: 'Rawabe', label: 'Rawabe' },
{ value: 'Gobuf', label: 'Gobuf' },
{ value: 'Kazi', label: 'Kazi' },
{ value: 'Dawal', label: 'Dawal' },
{ value: 'Panasi', label: 'Panasi' },
{ value: 'Cej', label: 'Cej' },
{ value: 'Bemab', label: 'Bemab' },
{ value: 'Quduja', label: 'Quduja' },
{ value: 'Pes', label: 'Pes' },
{ value: 'Nolita', label: 'Nolita' },
{ value: 'Wiz', label: 'Wiz' },
{ value: 'Danari', label: 'Danari' },
{ value: 'Fajo', label: 'Fajo' },
{ value: 'Tomu', label: 'Tomu' },
{ value: 'Cibi', label: 'Cibi' },
{ value: 'Qajoqu', label: 'Qajoqu' },
{ value: 'Yecab', label: 'Yecab' },
{ value: 'Vohomi', label: 'Vohomi' },
{ value: 'Baradi', label: 'Baradi' },
{ value: 'Dip', label: 'Dip' },
{ value: 'Zot', label: 'Zot' },
{ value: 'Mozewo', label: 'Mozewo' },
{ value: 'Facot', label: 'Facot' },
{ value: 'Nasime', label: 'Nasime' },
{ value: 'Mal', label: 'Mal' },
{ value: 'Bizu', label: 'Bizu' },
{ value: 'Qop', label: 'Qop' },
{ value: 'nan', label: 'nan' },
{ value: 'Moyu', label: 'Moyu' },
{ value: 'Vubugo', label: 'Vubugo' },
{ value: 'Zic', label: 'Zic' },
{ value: 'Nol', label: 'Nol' },
{ value: 'Xogem', label: 'Xogem' },
{ value: 'Noliqo', label: 'Noliqo' },
{ value: 'Lov', label: 'Lov' },
{ value: 'Toq', label: 'Toq' },
{ value: 'Sexob', label: 'Sexob' },
{ value: 'Selil', label: 'Selil' },
{ value: 'Gifop', label: 'Gifop' },
{ value: 'Xuwus', label: 'Xuwus' },
{ value: 'Yibege', label: 'Yibege' },
{ value: 'Xasu', label: 'Xasu' },
{ value: 'Xam', label: 'Xam' },
{ value: 'Gugen', label: 'Gugen' },
{ value: 'Momi', label: 'Momi' },
{ value: 'Qim', label: 'Qim' },
{ value: 'Fejo', label: 'Fejo' },
{ value: 'Rop', label: 'Rop' },
{ value: 'Lowi', label: 'Lowi' },
{ value: 'Gica', label: 'Gica' },
{ value: 'Xopag', label: 'Xopag' },
{ value: 'Coqupu', label: 'Coqupu' },
{ value: 'Diwej', label: 'Diwej' },
{ value: 'Kiwa', label: 'Kiwa' },
{ value: 'Lape', label: 'Lape' },
{ value: 'Fuheci', label: 'Fuheci' },
{ value: 'Jeqe', label: 'Jeqe' },
{ value: 'Lik', label: 'Lik' },
{ value: 'Neha', label: 'Neha' },
{ value: 'Qez', label: 'Qez' },
{ value: 'Pehu', label: 'Pehu' },
{ value: 'Wibabo', label: 'Wibabo' },
{ value: 'Tuz', label: 'Tuz' },
{ value: 'Reso', label: 'Reso' },
{ value: 'Run', label: 'Run' },
{ value: 'Waxe', label: 'Waxe' },
{ value: 'Kolo', label: 'Kolo' },
{ value: 'Des', label: 'Des' },
{ value: 'Yabebe', label: 'Yabebe' },
{ value: 'Deq', label: 'Deq' },
{ value: 'Ceh', label: 'Ceh' },
{ value: 'Metoju', label: 'Metoju' },
{ value: 'Behi', label: 'Behi' },
{ value: 'Maxenu', label: 'Maxenu' },
{ value: 'Vize', label: 'Vize' },
{ value: 'Joxoh', label: 'Joxoh' },
{ value: 'Jobi', label: 'Jobi' },
{ value: 'Fazi', label: 'Fazi' },
{ value: 'Rodiz', label: 'Rodiz' },
{ value: 'Nis', label: 'Nis' },
{ value: 'Quh', label: 'Quh' },
{ value: 'Roz', label: 'Roz' },
{ value: 'Rukopo', label: 'Rukopo' },
{ value: 'Few', label: 'Few' },
{ value: 'Zaqupi', label: 'Zaqupi' },
{ value: 'Newav', label: 'Newav' },
{ value: 'Casi', label: 'Casi' },
{ value: 'Qunir', label: 'Qunir' },
{ value: 'Samoh', label: 'Samoh' },
{ value: 'Cofo', label: 'Cofo' },
{ value: 'Wap', label: 'Wap' },
{ value: 'Howat', label: 'Howat' },
{ value: 'Panat', label: 'Panat' },
{ value: 'Yutica', label: 'Yutica' },
{ value: 'Zoke', label: 'Zoke' },
{ value: 'Yizu', label: 'Yizu' },
{ value: 'Tev', label: 'Tev' },
{ value: 'Yoyoke', label: 'Yoyoke' },
{ value: 'Medofu', label: 'Medofu' },
{ value: 'Rok', label: 'Rok' },
{ value: 'Piquf', label: 'Piquf' },
{ value: 'Xafodu', label: 'Xafodu' },
{ value: 'Duku', label: 'Duku' },
{ value: 'Lopob', label: 'Lopob' },
{ value: 'Buvipa', label: 'Buvipa' },
{ value: 'Ruga', label: 'Ruga' },
{ value: 'Xixa', label: 'Xixa' },
{ value: 'Yitev', label: 'Yitev' },
{ value: 'Kuhil', label: 'Kuhil' },
{ value: 'Celoji', label: 'Celoji' },
{ value: 'Domeza', label: 'Domeza' },
{ value: 'Bik', label: 'Bik' },
{ value: 'Kofisu', label: 'Kofisu' },
{ value: 'Bewito', label: 'Bewito' },
{ value: 'Seh', label: 'Seh' },
{ value: 'Dol', label: 'Dol' },
{ value: 'Ziz', label: 'Ziz' },
{ value: 'Pox', label: 'Pox' },
{ value: 'Nabar', label: 'Nabar' },
{ value: 'Nuq', label: 'Nuq' },
{ value: 'Lasi', label: 'Lasi' },
{ value: 'Gapuko', label: 'Gapuko' },
{ value: 'Gufis', label: 'Gufis' },
{ value: 'Gesez', label: 'Gesez' },
{ value: 'Wef', label: 'Wef' },
{ value: 'Fod', label: 'Fod' },
{ value: 'Nanux', label: 'Nanux' },
{ value: 'Havi', label: 'Havi' },
{ value: 'Saye', label: 'Saye' },
{ value: 'Lir', label: 'Lir' },
{ value: 'Naban', label: 'Naban' },
{ value: 'Wuj', label: 'Wuj' },
{ value: 'Wicol', label: 'Wicol' },
{ value: 'Soq', label: 'Soq' },
{ value: 'Hovo', label: 'Hovo' },
{ value: 'Nozo', label: 'Nozo' },
{ value: 'Bixef', label: 'Bixef' },
{ value: 'Wadu', label: 'Wadu' },
{ value: 'Jexa', label: 'Jexa' },
{ value: 'Kizom', label: 'Kizom' },
{ value: 'Toyoyo', label: 'Toyoyo' },
{ value: 'Xovefo', label: 'Xovefo' },
{ value: 'Ripe', label: 'Ripe' },
{ value: 'Bavu', label: 'Bavu' },
{ value: 'Koki', label: 'Koki' },
{ value: 'Seq', label: 'Seq' },
{ value: 'Qibu', label: 'Qibu' },
{ value: 'Wale', label: 'Wale' },
{ value: 'Mibeh', label: 'Mibeh' },
{ value: 'Kafu', label: 'Kafu' },
{ value: 'Soyup', label: 'Soyup' },
{ value: 'Jil', label: 'Jil' },
{ value: 'Gumigo', label: 'Gumigo' },
{ value: 'Jomita', label: 'Jomita' },
{ value: 'Haqita', label: 'Haqita' },
{ value: 'Sij', label: 'Sij' },
{ value: 'Fumoh', label: 'Fumoh' },
{ value: 'Kopo', label: 'Kopo' },
{ value: 'Faduj', label: 'Faduj' },
{ value: 'Kis', label: 'Kis' },
{ value: 'Cedaj', label: 'Cedaj' },
{ value: 'Mot', label: 'Mot' },
{ value: 'Puyafu', label: 'Puyafu' },
{ value: 'Hef', label: 'Hef' },
{ value: 'Tej', label: 'Tej' },
{ value: 'Macus', label: 'Macus' },
{ value: 'Yaj', label: 'Yaj' },
{ value: 'Deg', label: 'Deg' },
{ value: 'Teqi', label: 'Teqi' },
{ value: 'Mekez', label: 'Mekez' },
{ value: 'Lix', label: 'Lix' },
{ value: 'Femipu', label: 'Femipu' },
{ value: 'Figele', label: 'Figele' },
{ value: 'Badi', label: 'Badi' },
{ value: 'Medira', label: 'Medira' },
{ value: 'Cadi', label: 'Cadi' },
{ value: 'Gobu', label: 'Gobu' },
{ value: 'Peqiw', label: 'Peqiw' },
{ value: 'Vevu', label: 'Vevu' },
{ value: 'Dazab', label: 'Dazab' },
{ value: 'Xavuyu', label: 'Xavuyu' },
{ value: 'Godove', label: 'Godove' },
{ value: 'Pirabi', label: 'Pirabi' },
{ value: 'Pam', label: 'Pam' },
{ value: 'Sasada', label: 'Sasada' },
{ value: 'Hoyo', label: 'Hoyo' },
{ value: 'Deku', label: 'Deku' },
{ value: 'Cile', label: 'Cile' },
{ value: 'Dakufa', label: 'Dakufa' },
{ value: 'Nogati', label: 'Nogati' },
{ value: 'Waquq', label: 'Waquq' },
{ value: 'Yaka', label: 'Yaka' },
{ value: 'Fuko', label: 'Fuko' },
{ value: 'Roho', label: 'Roho' },
        ]}
    />
        </Form.Item>
        <Form.Item label="Do you want to live in an accommodation near beach?: " name="beach">
          <Radio.Group
          options={[
            { value: 1, label: 'Yes' },
            { value: 0, label: 'No' },
            { value: -1, label: 'I don\'t care' },
          ]}
          />
        </Form.Item>
        <Form.Item label="Do you want to live in an accommodation near ski place?: " name="ski">
          <Radio.Group
          options={[
            { value: 1, label: 'Yes' },
            { value: 0, label: 'No' },
            { value: -1, label: 'I don\'t care' },
          ]}
          />
        </Form.Item>
        <Form.Item label="Do you want to live in an accommodation in downtown?: " name="center">
          <Radio.Group
          options={[
            { value: 1, label: 'Yes' },
            { value: 0, label: 'No' },
            { value: -1, label: 'I don\'t care' },
          ]}
          />
        </Form.Item>
        <Form.Item label="In which month will you start your trip?: " name="months">
          <Select
          showSearch
          style={{ width: 250 }}
          options={[
            { value: '1', label: 'January' },
            { value: '2', label: 'February' },
            { value: '3', label: 'March' },
            { value: '4', label: 'April' },
            { value: '5', label: 'May' },
            { value: '6', label: 'June' },
            { value: '7', label: 'July' },
            { value: '8', label: 'August' },
            { value: '9', label: 'September' },
            { value: '10', label: 'October' },
            { value: '11', label: 'November' },
            { value: '12', label: 'December' },
        ]}
    />
        </Form.Item>
        <Form.Item label="How many nights would you spend there?: " name="nights">
          <InputNumber min={1} defaultValue={1}/>
        </Form.Item>
        <Form.Item label="Requirement: " name="requirement">
          <Input.TextArea 
    placeholder="You can write your requirement in natural language here" 
    autoSize 
    />
        </Form.Item>
        <Form.Item label=" ">
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
    </Form.Item>
        </Form>
    )} 
        {currentPage === "result" && (
        <div style={{ maxWidth: 700, margin: "0 auto", width: "100%" }}>
        <Card title="Our recommendation: ">{result.response}</Card>
        <Divider>Relevant reviews</Divider>
        {result.target_reviews?.map((review: any, i: any) => (
        <Card title={review.title}>
          <p><b>Accommodation ID: </b>{review.accommodation_id}</p>
          <p><b>Pro: </b>{review.pro}</p>
          <p><b>Contra: </b>{review.contra}</p>
        </Card>
        ))}
        <Divider>Other reviews</Divider>
        {result.other_reviews?.map((review: any, i: any) => (
        <Card title={review.title}>
          <p><b>Accommodation ID: </b>{review.accommodation_id}</p>
          <p><b>Pro: </b>{review.pro}</p>
          <p><b>Contra: </b>{review.contra}</p>
        </Card>
        ))}
        </div>
    )}
    {currentPage === "loading" && (
      <div style={{textAlign: 'center', marginTop: 48}}>
      <h2>Waiting for the LLM to generate answer...</h2>
      <Spin tip="Waiting for the LLM to generate answer..." size="large" />
      </div>
    )}
      </div>
    </main>
  );
}

interface Review {
  accommodation_id: number;
  title: string;
  pro: string;
  contra: string;
}

interface Answer {
  response: string;
  target_reviews: Review[];
  other_reviews: Review[];
}