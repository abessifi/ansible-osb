# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'spec_helper'
require 'wls_params'

describe "Check OSB installation" do

  describe file(OSB_HOME_DIR) do
    it { should be_directory }
    it { should be_owned_by 'oracle' }
    it { should be_grouped_into 'oinstall' }
  end

end
