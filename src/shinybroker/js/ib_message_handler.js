let sec_def_opt_params_buf = [];
let contract_data_buf = [];
Shiny.addCustomMessageHandler('1', function(msg) {
        Shiny.setInputValue('tick_price', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('2', function(msg) {
        Shiny.setInputValue('tick_size', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('4', function(msg) {
        Shiny.setInputValue('error_message', msg, {priority: 'event'});
        if (['200', '321', '322', '2130', '10089'].includes(msg[2])) {
            Shiny.setInputValue(
                'error_notification', msg[3], {priority: 'event'}
            );
        }
    }
);
Shiny.addCustomMessageHandler('9', function(msg) {
        Shiny.setInputValue('next_valid_id', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('10', function(msg) {
        msg.shift(); // don't need reqID (first element)
        console.log(msg)
        contract_data_buf.push(msg);
    }
);
Shiny.addCustomMessageHandler('15', function(msg) {
        Shiny.setInputValue('managed_accounts', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('17', function(msg) {
        Shiny.setInputValue('historical_data', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('18', function(msg) {
        msg.shift(); // don't need reqID (first element)
        console.log(msg)
        contract_data_buf.push(msg);
    }
);
Shiny.addCustomMessageHandler('45', function(msg) {
        Shiny.setInputValue('tick_generic', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('46', function(msg) {
        Shiny.setInputValue('tick_string', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('49', function(msg) {
        Shiny.setInputValue('current_time', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('52', function(msg) {
        Shiny.setInputValue('contract_details', contract_data_buf);
        contract_data_buf = [];
    }
);
Shiny.addCustomMessageHandler('58', function(msg) {
        Shiny.setInputValue(
            'market_data_type_response', msg, {priority: 'event'}
        );
    }
);
Shiny.addCustomMessageHandler('75', function(msg) {
        msg.shift(); // don't need reqID (first element)
        sec_def_opt_params_buf.push(msg);
    }
);
Shiny.addCustomMessageHandler('76', function(msg) {
        Shiny.setInputValue('sec_def_opt_params', sec_def_opt_params_buf);
        sec_def_opt_params_buf = [];
    }
);
Shiny.addCustomMessageHandler('79', function(msg) {
        Shiny.setInputValue('symbol_samples', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('81', function(msg) {
        Shiny.setInputValue('tick_req_params', msg, {priority: 'event'});
    }
);
Shiny.addCustomMessageHandler('90', function(msg) {
        Shiny.setInputValue('historical_data_update', msg, {priority: 'event'});
    }
);
